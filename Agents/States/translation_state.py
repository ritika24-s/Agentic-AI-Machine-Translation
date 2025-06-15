from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

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
    source_text: str  # the source text to be translated
    source_language: str  # the language of the source text
    target_language: str  # the language to translate the source text to
    translated_text: str  # the translated text
    confidence_score: float  # the confidence score of the translation
    conversation_context: List[str]  # Previous translations for context
    needs_human_review: bool  # whether the translation needs human review
    error_messages: List[str]  # error messages from the translation system