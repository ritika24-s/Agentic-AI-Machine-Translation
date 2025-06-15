"""
This module contains the language detection node functions.
"""

from AgentArchitecture.States.translation_state import TranslationState
from Translator.libre_translate import LibreTranslate

def language_detection_node(state: TranslationState) -> dict:
    """
    This node is used to detect the language of the text.
    Functions receive the current state as input DeepWiki
    Return a dictionary with updates to state fields
    LangGraph automatically merges your updates with existing state
    Always include helpful messages for debugging and monitoring

    Args:
        state: TranslationState: contains the state of the translation system.

    Returns:
        dict: 
    """
    if state.get("source_language"):
        detected_lang = state.get("source_language")
    else:
        # call the language detection model
        detected_lang = LibreTranslate.libre_translate(state.get("source_text"), detect_language=True)
    
    return {
        "source_language": detected_lang,
        "messages": [f"Detected language: {detected_lang}"]
    }


def language_detection_node_with_retry(state: TranslationState) -> dict:
    """
    This node is used to detect the language of the text with retry.
    """
    return state