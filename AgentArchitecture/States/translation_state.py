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
    conversation_context = get_conversation_context(translation_state)
    relevant_context = []
    
    # Look for related previous translations
    for previous_translation in conversation_context[-5:]:  # Last 5 for context
        if any(word in source_text.lower() for word in previous_translation.split()):
            relevant_context.append(previous_translation)
    return relevant_context