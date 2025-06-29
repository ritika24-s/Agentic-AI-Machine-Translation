from dataclasses import dataclass
from enum import Enum
from typing import TypedDict, Annotated, List, Optional, Dict, Any
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class TranslationComplexity(Enum):
    SIMPLE = "simple"
    TECHNICAL = "technical"
    CREATIVE = "creative"
    FORMAL = "formal"

class TranslationStatus(Enum):
    PENDING = "pending"
    ROUTING = "routing"
    TRANSLATING = "translating"
    EDITING = "editing"
    QUALITY_CHECK = "quality_check"
    COMPLETED = "completed"
    FAILED = "failed"


class TranslationState(TypedDict):
    """
    The shared memory for machine translation system
    Why this structure works: 
    - messages uses add_messages to automatically append new conversation turns. 
    - Each specialist can read the full context and update their specific fields. 
    - The orchestrator tracks overall progress through confidence_score and needs_human_review
    """
    # messages uses add_messages to automatically append new conversation turns
    messages: Annotated[List[BaseMessage], add_messages]

    # input
    source_text: str  # the source text to be translated
    source_language: str  # the language of the source text
    target_language: str  # the language to translate the source text to

    # Processing
    complexity_analysis: Optional[Dict[str, Any]]
    conversation_context: List[str]  # Previous translations for context
    context_data: Optional[Dict[str, Any]]
    translation_candidates: List[Dict[str, Any]]

    # Quality assessment
    quality_scores: Optional[Dict[str, float]]
    quality_issues: List[str]

    # output
    translated_text: str  # the translated text
    confidence_score: float  # the confidence score of the translation
    needs_human_review: bool  # whether the translation needs human review

    # Metadata
    processing_time: float
    agents_involved: List[str]

    # error handling
    error_messages: List[str]  # error messages from the translation system


@dataclass
class QualityMetrics:
    """Quality assessment metrics"""
    accuracy_score: float
    fluency_score: float
    cultural_appropriateness: float
    terminology_consistency: float
    overall_score: float
    

@dataclass  
class AgentPerformance:
    """Track individual agent performance"""
    agent_id: str
    processing_time: float
    success_rate: float
    quality_contribution: float


# Helper class
class TranslationStateHelper:
    """
    Helper functions for the translation state
    """
    def get_initial_translation_state(data: dict) -> TranslationState:
        """
        Initialize a new translation state
        """
        return TranslationState({
                    "messages": [],
                    "source_text": data.get("source_text", ""),
                    "source_language": data.get("source_language", "auto"),
                    "target_language": data.get("target_language", "es"),
                    "translated_text": "",
                    "confidence_score": 0.0,
                    "conversation_context": [],
                    "needs_human_review": False,
                    "error_messages": []
                })


    def get_conversation_context(translation_state: TranslationState) -> List[str]:
        """
        Get the conversation context from the translation state
        """
        return translation_state.get("conversation_context", [])


    def get_relevant_context(translation_state: TranslationState) -> List[str]:
        """
        Get the relevant context from the translation state
        """
        source_text = translation_state["source_text"]
        conversation_context = TranslationStateHelper.get_conversation_context(translation_state)
        relevant_context = []
        
        # Look for related previous translations
        for previous_translation in conversation_context[-5:]:  # Last 5 for context
            if any(word in source_text.lower() for word in previous_translation.split()):
                relevant_context.append(previous_translation)
        return relevant_context