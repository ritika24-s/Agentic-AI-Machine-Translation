from agent_architecture.States.translation_state import TranslationState


def target_language_node(state: TranslationState, target_language: str="es") -> dict:
    """
    This node is used to set the target language.
    """
    return {
        "target_language": target_language,
        "messages": [f"Target language: {target_language}"]
    }
