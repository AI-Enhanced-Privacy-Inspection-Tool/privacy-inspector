import json
from datetime import datetime
from typing import List, Dict
from google import genai
from google.genai import types

import config.settings as settings
from .prompts import create_privacy_analysis_prompt
from .models import (
    PrivacyDataItem,
    DataClassification,
    RiskAssessment,
    ActionSuggestion,
    AnalyzedDataItem,
    AIAnalysisResponse,
    DataSensitivityLevel,
    RiskLevel
)


class AIAnalyzer:
    
    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("Need GOOGLE_API_KEY in .env file!")
        
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        self.model = "models/gemini-3-flash-preview"
    
    def analyze_items(self, data_items: List[PrivacyDataItem]) -> AIAnalysisResponse:
        analyzed = []
        
        for item in data_items:
            try:
                result = self._analyze_one_item(item)
                analyzed.append(result)
            except Exception as e:
                print(f"Error analyzing {item.name}: {e}")
                continue
        
        summary = self._make_summary(analyzed)
        recommendations = self._make_recommendations(analyzed)
        
        return AIAnalysisResponse(
            total_items=len(analyzed),
            analyzed_items=analyzed,
            summary=summary,
            recommendations=recommendations
        )
    
    def _analyze_one_item(self, item: PrivacyDataItem) -> AnalyzedDataItem:
        
        prompt = create_privacy_analysis_prompt(
            data_name=item.name,
            data_value=item.value,
            data_type=item.data_type.value,
            domain=item.domain
        )
        
        ai_response = self._call_gemini(prompt)
        classification, risk, suggestions = self._parse_response(ai_response)
        
        return AnalyzedDataItem(
            name=item.name,
            value=item.value,
            data_type=item.data_type,
            domain=item.domain,
            classification=classification,
            risk_assessment=risk,
            suggestions=suggestions,
            analyzed_at=datetime.now().isoformat(),
            analysis_id=f"analysis_{datetime.now().timestamp()}"
        )
    
    def _call_gemini(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=1500,
            )
        )
        return response.text
    
    def _parse_response(self, ai_text: str):
        try:
            clean_text = ai_text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.startswith("```"):
                clean_text = clean_text[3:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            clean_text = clean_text.strip()
            
            data = json.loads(clean_text)
            
            classification = DataClassification(
                contains_pii=data["contains_pii"],
                pii_types=data.get("pii_types", []),
                is_tracking_data=data.get("is_tracking", False),
                sensitivity_level=DataSensitivityLevel(data["sensitivity"]),
                confidence_score=0.9,
                reasoning=data["explanation"]
            )
            
            risk = RiskAssessment(
                risk_level=RiskLevel(data["risk_level"]),
                risk_score=float(data["risk_score"]),
                risk_factors=data.get("risks", []),
                potential_threats=data.get("risks", []),
                data_leakage_likelihood=data["risk_level"]
            )
            
            suggestions = [ActionSuggestion(
                action=data["recommendation"],
                priority=data["risk_level"],
                reasoning=data["why_recommendation"],
                steps=[data["why_recommendation"]]
            )]
            
            return classification, risk, suggestions
            
        except Exception as e:
            print(f"Failed to parse AI response: {e}")
            print(f"Response was: {ai_text}")
            return self._fallback_analysis()
    
    def _fallback_analysis(self):
        classification = DataClassification(
            contains_pii=False,
            pii_types=[],
            is_tracking_data=False,
            sensitivity_level=DataSensitivityLevel.LOW,
            confidence_score=0.5,
            reasoning="Could not complete analysis"
        )
        
        risk = RiskAssessment(
            risk_level=RiskLevel.LOW,
            risk_score=2.0,
            risk_factors=["Analysis incomplete"],
            potential_threats=[],
            data_leakage_likelihood="low"
        )
        
        suggestions = [ActionSuggestion(
            action="review",
            priority="medium",
            reasoning="Manual review needed",
            steps=["Check this item manually"]
        )]
        
        return classification, risk, suggestions
    
    def _make_summary(self, items: List[AnalyzedDataItem]) -> Dict:
        if not items:
            return {
                "total_items": 0,
                "pii_count": 0,
                "tracking_count": 0,
                "high_risk_count": 0,
                "avg_risk_score": 0
            }
        
        pii_count = sum(1 for i in items if i.classification.contains_pii)
        tracking_count = sum(1 for i in items if i.classification.is_tracking_data)
        high_risk = sum(1 for i in items if i.risk_assessment.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL])
        avg_score = sum(i.risk_assessment.risk_score for i in items) / len(items)
        
        return {
            "total_items": len(items),
            "pii_count": pii_count,
            "tracking_count": tracking_count,
            "high_risk_count": high_risk,
            "avg_risk_score": round(avg_score, 2),
            "risk_breakdown": self._count_risk_levels(items),
            "sensitivity_breakdown": self._count_sensitivity_levels(items)
        }
    
    def _count_risk_levels(self, items):
        counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        for item in items:
            counts[item.risk_assessment.risk_level.value] += 1
        return counts
    
    def _count_sensitivity_levels(self, items):
        counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        for item in items:
            counts[item.classification.sensitivity_level.value] += 1
        return counts
    
    def _make_recommendations(self, items: List[AnalyzedDataItem]) -> List[str]:
        if not items:
            return ["No data to analyze"]
        
        recs = []
        
        critical = [i for i in items if i.risk_assessment.risk_level == RiskLevel.CRITICAL]
        high_risk = [i for i in items if i.risk_assessment.risk_level == RiskLevel.HIGH]
        
        if critical:
            recs.append(f"{len(critical)} CRITICAL risk items found - take action immediately")
        if high_risk:
            recs.append(f"{len(high_risk)} high risk items detected - review these soon")
        
        pii_items = [i for i in items if i.classification.contains_pii]
        if pii_items:
            recs.append(f"Found {len(pii_items)} items with personal information")
        
        tracking = [i for i in items if i.classification.is_tracking_data]
        if tracking:
            recs.append(f"{len(tracking)} tracking/analytics items found")
        
        if not recs:
            recs.append("No major privacy concerns detected")
        
        return recs


analyzer = AIAnalyzer()
