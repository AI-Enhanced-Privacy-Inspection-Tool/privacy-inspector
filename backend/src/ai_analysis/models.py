from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class DataSensitivityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DataType(str, Enum):
    COOKIE = "cookie"
    LOCAL_STORAGE = "local_storage"
    SESSION_STORAGE = "session_storage"
    CACHE = "cache"
    CONFIG_FILE = "config_file"
    DATABASE = "database"
    OTHER = "other"


class PrivacyDataItem(BaseModel):
    name: str = Field(..., description="Name or key of the data item")
    value: str = Field(..., description="Value or content of the data item")
    data_type: DataType = Field(..., description="Type of data (cookie, storage, etc.)")
    domain: Optional[str] = Field(None, description="Domain or source of the data")
    expiration: Optional[str] = Field(None, description="Expiration date/time if applicable")
    metadata: Optional[dict] = Field(default_factory=dict, description="Additional metadata")


class AIAnalysisRequest(BaseModel):
    data_items: List[PrivacyDataItem] = Field(..., description="List of privacy data items to analyze")


class DataClassification(BaseModel):
    contains_pii: bool = Field(..., description="Whether the data contains Personally Identifiable Information")
    pii_types: List[str] = Field(default_factory=list, description="Types of PII detected (e.g., email, phone, address)")
    is_tracking_data: bool = Field(..., description="Whether this is tracking/analytics data")
    sensitivity_level: DataSensitivityLevel = Field(..., description="Overall sensitivity classification")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="AI confidence in classification (0-1)")
    reasoning: str = Field(..., description="AI explanation for the classification")


class RiskAssessment(BaseModel):
    risk_level: RiskLevel = Field(..., description="Overall risk level")
    risk_score: float = Field(..., ge=0.0, le=10.0, description="Risk score (0-10)")
    risk_factors: List[str] = Field(default_factory=list, description="Identified risk factors")
    potential_threats: List[str] = Field(default_factory=list, description="Potential security/privacy threats")
    data_leakage_likelihood: str = Field(..., description="Likelihood of data leakage (low/medium/high)")


class ActionSuggestion(BaseModel):
    action: str = Field(..., description="Recommended action (e.g., 'delete', 'encrypt', 'review')")
    priority: str = Field(..., description="Priority level (low/medium/high/critical)")
    reasoning: str = Field(..., description="Why this action is recommended")
    steps: List[str] = Field(default_factory=list, description="Specific steps to take")


class AnalyzedDataItem(BaseModel):
    name: str
    value: str
    data_type: DataType
    domain: Optional[str] = None
    classification: DataClassification
    risk_assessment: RiskAssessment
    suggestions: List[ActionSuggestion]
    analyzed_at: str
    analysis_id: str


class AIAnalysisResponse(BaseModel):
    total_items: int = Field(..., description="Total number of items analyzed")
    analyzed_items: List[AnalyzedDataItem] = Field(..., description="Detailed analysis for each item")
    summary: dict = Field(..., description="Overall summary of findings")
    recommendations: List[str] = Field(default_factory=list, description="Top-level recommendations")
