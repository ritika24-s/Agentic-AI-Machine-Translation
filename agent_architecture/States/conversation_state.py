from typing import Any
from typing_extensions import TypedDict


class ConversationState(TypedDict):
    """
    State management for Conversation Context
    Store previous translations to maintain consistency
    """
    translation_memory: dict[tuple[str, str], str]  # (source_text, target_language) -> translated_text
    terminology_glossary: dict[str, str]  # specialized terms
    user_preferences: dict[str, Any]  # formality, style choices
    session_context: str  # current conversation topic
    
def get_initial_conversation_state() -> ConversationState:
    """
    Initialize a new conversation state
    """
    return ConversationState({
            "translation_memory": {},
            "terminology_glossary": {},
            "user_preferences": {},
            "session_context": ""
        })


def get_translation_memory(conversation_state: ConversationState) -> dict:
    """
    Get the translation memory from the conversation state
    """
    return conversation_state.get("translation_memory", {})


def get_repeated_phrases(conversation_state: ConversationState, source_text: str, target_language: str) -> list[tuple[str, str, str]]:
    """
    Get the repeated phrases from the conversation state
    """
    translation_memory = get_translation_memory(conversation_state)
    repeated_phrases = []
    for phrase in source_text.split('.'):
        phrase = phrase.strip()
        if (phrase, target_language) in translation_memory:
            repeated_phrases.append((phrase, target_language, translation_memory[(phrase, target_language)]))

    return repeated_phrases