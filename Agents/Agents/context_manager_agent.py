"""
The Context Manager maintains conversation coherence and translation consistency
"""

from Agents.States.translation_state import TranslationState
from Agents.States.conversation_state import ConversationState


def context_manager_agent(translation_state: TranslationState, conversation_state: ConversationState) -> dict:
    """
    Manage conversation context and translation memory
    Context Preservation Techniques:
    - Sliding window: Keep recent context without overwhelming memory
    - Semantic similarity: Match content themes across translations
    - Terminology consistency: Ensure repeated terms translate consistently

    Args:
        state (TranslationState): The current state of the translation process

    Returns:
        dict: A dictionary containing the context strategy, relevant context, and repeated phrases
    """
    source_text = translation_state["source_text"]
    target_language = translation_state["target_language"]
    
    # Retrieve relevant context from conversation history
    conversation_context = translation_state.get("conversation_context", [])
    relevant_context = []
    
    # Look for related previous translations
    for previous_translation in conversation_context[-5:]:  # Last 5 for context
        if any(word in source_text.lower() for word in previous_translation.split()):
            relevant_context.append(previous_translation)
    
    # Check translation memory for consistency
    translation_memory = conversation_state.get("translation_memory", {})
    repeated_phrases = []
    for phrase in source_text.split('.'):
        phrase = phrase.strip()
        if (phrase, target_language) in translation_memory:
            repeated_phrases.append((phrase, translation_memory[(phrase, target_language)]))
    
    # Determine context strategy
    if relevant_context:
        context_strategy = "conversation_aware"
    elif repeated_phrases:
        context_strategy = "consistency_enforced"
    else:
        context_strategy = "standalone"
    
    return {
        "context_strategy": context_strategy,
        "relevant_context": relevant_context,
        "repeated_phrases": repeated_phrases,
        "messages": [f"Context Manager: Using {context_strategy} strategy"]
    }