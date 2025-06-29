"""
The Router Agent is the system's traffic controller, deciding how to handle each translation request

Role: The "CEO" of the translation company - makes strategic decisions about how to handle each translation request.

Core Intelligence:
- Complexity Analysis: Distinguishes between "Hello" (simple) vs "Please review the arbitration clause in section 4.2b" (complex legal)
- Domain Detection: Recognizes medical terminology, legal jargon, technical specifications, creative writing
- Urgency Assessment: Real-time chat vs document translation vs batch processing
- Resource Allocation: Which agents need to be involved and in what sequence

Decision Framework:
- Simple Text → Direct to Translation Specialist (fast path)
- Technical/Domain-Specific → Context Orchestrator + Specialized Translation Specialist
- Conversational → Full agent team with memory management
- Creative/Marketing → Cultural adaptation pathway with Quality Guardian emphasis

Key Innovation: Unlike traditional MT that treats all text the same, this agent creates custom workflows for each request type.
"""
from agent_architecture.States.translation_state import TranslationState


TECHNICAL_TERMS = ["api", "database", "algorithm", "function"]
FORMAL_LANGUAGE = ["dear sir", "sincerely", "respectfully"]


def get_complexity(text: str) -> tuple[str, str]:
    """
    Get the complexity of the text
    Args:
        text (str): The text to analyze

    Returns:
        tuple[str, str]: A tuple containing the complexity and translation approach
    """
    text_length = len(text.split())

    # Todo: Extend the router to detect other text types (questions, commands, creative content)
    # and set appropriate handling strategies.

    # Analyze text characteristics
    has_technical_terms = any(term in text.lower() for term in TECHNICAL_TERMS)
    has_formal_language = any(phrase in text.lower() for phrase in FORMAL_LANGUAGE)

    # Determine routing strategy
    if text_length > 100:
        complexity = "high"
        translation_approach = "paragraph_by_paragraph"
    elif has_technical_terms:
        complexity = "technical"  
        translation_approach = "terminology_focused"
    elif has_formal_language:
        complexity = "formal"
        translation_approach = "style_preserved"
    else:
        complexity = "standard"
        translation_approach = "direct_translation"

    return complexity, translation_approach


def router_agent(state: TranslationState) -> dict:
    """
    Route translation requests based on complexity and requirements
    The router makes intelligent decisions based on observable text characteristics. 
    It sets strategy flags that other agents can reference, 
    creating a coordinated approach to translation challenges.
    Args:
        state (TranslationState): The current state of the translation process

    Returns:
        dict: A dictionary containing the complexity and translation approach
    """
    text = state["source_text"]
    complexity, translation_approach = get_complexity(text)
  
    return {
        "complexity": complexity,
        "translation_approach": translation_approach,
        "messages": [f"Router: Selected {translation_approach} approach for {complexity} text"]
    }