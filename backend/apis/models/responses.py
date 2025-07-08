from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class AgentActivity(BaseModel):
    """Individual agent activity information"""
    agent_name: str = Field(..., description="Name of the agent")
    status: str = Field(..., description="Current status")
    start_time: datetime = Field(..., description="When agent started processing")
    end_time: Optional[datetime] = Field(None, description="When agent finished")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Agent confidence score")
    message: Optional[str] = Field(None, description="Agent status message")


class QualityMetrics(BaseModel):
    """Translation quality assessment"""
    overall_score: float = Field(..., ge=0.0, le=1.0)
    fluency_score: float = Field(..., ge=0.0, le=1.0)
    accuracy_score: float = Field(..., ge=0.0, le=1.0)
    consistency_score: float = Field(..., ge=0.0, le=1.0)
    confidence_level: str = Field(..., description="High/Medium/Low confidence")


class TranslationResponse(BaseModel):
    """Single translation response"""
    request_id: str = Field(..., description="Unique request identifier")
    translated_text: str = Field(..., description="Translated text")
    source_language: str = Field(..., description="Detected/provided source language")
    target_language: str = Field(..., description="Target language")
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    agent_activities: List[AgentActivity] = Field(default_factory=list)
    quality_metrics: QualityMetrics
    processing_time: float = Field(..., description="Processing time in seconds")
    complexity: str = Field(..., description="Detected text complexity")
    created_at: datetime = Field(default_factory=datetime.now)


class BatchTranslationResponse(BaseModel):
    """Batch translation response"""
    batch_id: str
    total_items: int
    completed_items: int
    failed_items: int
    results: List[TranslationResponse]
    overall_processing_time: float


class DocumentStatus(BaseModel):
    """Document processing status"""
    task_id: str
    status: str  # "processing", "completed", "failed"
    progress: float = Field(..., ge=0.0, le=100.0)
    current_page: Optional[int] = None
    total_pages: Optional[int] = None
    agent_status: Dict[str, str] = Field(default_factory=dict)
    estimated_completion: Optional[datetime] = None


class LanguagePair(BaseModel):
    """Supported language pair"""
    source: str
    target: str
    quality_score: float
    agent_preference: str  # Which agent handles this pair best


class SupportedLanguagesResponse(BaseModel):
    """All supported language pairs"""
    languages: List[LanguagePair]
    total_pairs: int


class ErrorResponse(BaseModel):
    """Standardized error response"""
    error: str
    detail: str
    request_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)