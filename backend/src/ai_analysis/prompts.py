def create_privacy_analysis_prompt(data_name, data_value, data_type, domain=None):
    
    prompt = f"""You are analyzing data found on a user's computer for privacy and security risks.

DATA TO ANALYZE:
- Name: {data_name}
- Value: {data_value[:300]}{"..." if len(data_value) > 300 else ""}
- Type: {data_type}
- Source: {domain if domain else "Unknown"}

YOUR TASK:
Analyze this data and help the user understand:
1. Does it contain personal information? (email, phone, name, address, credit card, SSN, etc.)
2. Is it tracking/analytics data? (cookies that track user behavior across sites)
3. What are the privacy risks?
4. What should the user do about it?

RESPOND IN THIS JSON FORMAT:
{{
    "contains_pii": true or false,
    "pii_types": ["email", "phone", etc.] or [],
    "is_tracking": true or false,
    "sensitivity": "low" or "medium" or "high" or "critical",
    "risk_level": "low" or "medium" or "high" or "critical",
    "risk_score": number from 0 to 10,
    "explanation": "explain what this data is and why it matters",
    "risks": ["list", "of", "specific", "risks"],
    "recommendation": "what the user should do (delete/keep/encrypt/review)",
    "why_recommendation": "explain why you recommend this action"
}}

IMPORTANT:
- Be specific about what personal info you detect
- Explain risks in simple terms
- Give actionable advice
- "low" sensitivity = harmless data, "high" = personal info, "critical" = financial/health data

Respond ONLY with the JSON, nothing else."""

    return prompt
