from fastapi import Depends, HTTPException, status
import uuid
from typing import Generator


from agent_architecture.agent_workflow import create_translation_system
from agent_architecture.States.translation_state import TranslationState


async def get_translation_service():
    """Dependency to get translation service instance"""
    return create_translation_system()


async def generate_request_id() -> str:
    """Generate unique request ID for tracking"""
    return str(uuid.uuid4())


async def validate_language_pair(source: str, target: str):
    """Validate language pair is supported"""
    supported_languages = ["en", "es", "fr", "de", "zh", "ja"]
    
    if source not in supported_languages:
        raise HTTPException(
            status_code=400,
            detail=f"Source language '{source}' not supported"
        )
    
    if target not in supported_languages:
        raise HTTPException(
            status_code=400,
            detail=f"Target language '{target}' not supported"
        )
    
    if source == target:
        raise HTTPException(
            status_code=400,
            detail="Source and target languages cannot be the same"
        )