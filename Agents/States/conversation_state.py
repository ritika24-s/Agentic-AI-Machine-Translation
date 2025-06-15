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
    