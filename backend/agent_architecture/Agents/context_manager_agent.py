"""
The Context Manager maintains conversation coherence and translation consistency
Role: The "Memory Manager" - ensures translations feel natural and consistent across conversations.

Contextual Intelligence:
- Conversation Threading: Remembers that "it" in message 5 refers to "the contract" from message 2
- Terminology Consistency: If "user interface" is translated as "interfaz de usuario" once, maintains this choice
- Cultural Context Mapping: Knows that German business emails are more formal than American ones
- Temporal Awareness: Understands that "tomorrow" depends on when the conversation started

Memory Architecture:
- Short-term: Current conversation flow and immediate references
- Medium-term: Session terminology preferences and style choices
- Long-term: User/domain-specific translation patterns and preferred terminology

Strategic Value: This is what makes the system "conversational" rather than just translating isolated sentences.
"""

from agent_architecture.States.translation_state import TranslationState, get_relevant_context
from agent_architecture.States.conversation_state import ConversationState, get_initial_conversation_state, get_repeated_phrases


def get_context_strategy(relevant_context: list[str], repeated_phrases: list[tuple[str, str, str]]) -> str:
    """
    Get the context strategy based on the relevant context and repeated phrases
    """
    if relevant_context:
        return "conversation_aware" # Use the last 5 translations for context
    elif repeated_phrases:
        return "consistency_enforced" # Ensure consistent translation of repeated phrases
    else:
        return "standalone" # simply translate


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

    # Handle case where conversation_state is None
    if not conversation_state:
        conversation_state = get_initial_conversation_state()
    
    # Retrieve relevant context from conversation history
    relevant_context = get_relevant_context(translation_state)
    
    # Check translation memory for consistency
    repeated_phrases = get_repeated_phrases(conversation_state, source_text, target_language)
    
    # Determine context strategy
    context_strategy = get_context_strategy(relevant_context, repeated_phrases)
    
    return {
        "context_strategy": context_strategy,
        "relevant_context": relevant_context,
        "repeated_phrases": repeated_phrases,
        "messages": [f"Context Manager: Using {context_strategy} strategy"]
    }