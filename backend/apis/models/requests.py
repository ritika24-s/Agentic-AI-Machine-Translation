from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from enum import Enum
from translation_services.supported_languages import LanguageCode


class ComplexityLevel(str, Enum):
    """Text complexity levels for agent routing"""
    SIMPLE = "simple"
    TECHNICAL = "technical"
    CREATIVE = "creative"
    FORMAL = "formal"


class TranslationRequest(BaseModel):
    """Single text translation request"""
    text: str = Field(..., min_length=1, max_length=10000, description="Text to translate")
    source_language: LanguageCode = Field(..., description="Source language code")
    target_language: LanguageCode = Field(..., description="Target language code")
    context: Optional[str] = Field(None, description="Additional context for translation")
    preserve_formatting: bool = Field(False, description="Preserve original formatting")
    
    @field_validator('text')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty or only whitespace')
        return v.strip()
    
    @field_validator('target_language')
    def validate_different_languages(cls, v, values):
        if 'source_language' in values and v == values['source_language']:
            raise ValueError('Source and target languages must be different')
        return v


class BatchTranslationRequest(BaseModel):
    """Multiple text translation request"""
    texts: List[str] = Field(..., min_items=1, max_items=50)
    source_language: LanguageCode
    target_language: LanguageCode
    context: Optional[str] = None
    

class ConversationUpdateRequest(BaseModel):
    """Update conversation context"""
    conversation_id: str = Field(..., description="Unique conversation identifier")
    context: Dict[str, Any] = Field(..., description="Conversation context data")
    preferences: Optional[Dict[str, Any]] = Field(None, description="User preferences")

class FeedbackRequest(BaseModel):
    """Quality feedback for translations"""
    translation_id: str
    rating: int = Field(..., ge=1, le=5, description="Quality rating (1-5)")
    feedback_text: Optional[str] = Field(None, max_length=1000)
    suggested_translation: Optional[str] = Field(None)