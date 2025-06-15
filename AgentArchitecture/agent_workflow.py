"""
System Benefits:

Intelligent routing: Different strategies for different text types
Quality assurance: Automatic retry loops and human escalation
Context awareness: Maintains consistency across conversations
Error resilience: Multiple fallback strategies prevent failures
"""
# Third-party imports
from langgraph.graph import StateGraph, START, END

# Local imports
from AgentArchitecture.States.translation_state import TranslationState, get_initial_translation_state
from AgentArchitecture.States.conversation_state import ConversationState, get_initial_conversation_state
from AgentArchitecture.Agents.router_agent import router_agent
from AgentArchitecture.Agents.context_manager_agent import context_manager_agent
from AgentArchitecture.Agents.translation_agent import translation_agent
from AgentArchitecture.Agents.qa_agent import qa_agent
from AgentArchitecture.Agents.orchestrator_agent import orchestrator_agent


def decide_next_step(state: TranslationState) -> str:
    """Conditional routing logic for quality-based workflow"""
    next_action = state.get("next_action", "complete")
    
    if next_action == "retry":
        return "translator"  # Try translation again
    elif next_action == "human_review":
        return "orchestrator"  # Send to orchestrator for human handling
    else:
        return "orchestrator"  # Normal completion

def create_translation_system():
    """Build the complete multi-agent translation system"""
    
    # Create the workflow graph
    workflow = StateGraph(TranslationState)

    # Wrap context manager to handle the conversation state
    def context_manager_wrapper(state: TranslationState) -> dict:
        # Create empty conversation state if needed
        conversation_state = get_initial_conversation_state()
        return context_manager_agent(state, conversation_state)
    
    # Add all agents
    workflow.add_node("router", router_agent)
    workflow.add_node("context_manager", context_manager_wrapper)  # Use wrapper
    workflow.add_node("translator", translation_agent)
    workflow.add_node("qa_checker", qa_agent)
    workflow.add_node("orchestrator", orchestrator_agent)
    
    # Define workflow edges
    workflow.add_edge(START, "router")
    workflow.add_edge("router", "context_manager")
    workflow.add_edge("context_manager", "translator")
    workflow.add_edge("translator", "qa_checker")
    
    # Conditional routing based on QA results
    workflow.add_conditional_edges(
        "qa_checker",
        decide_next_step,
        {
            "translator": "translator",  # Retry translation
            "orchestrator": "orchestrator"  # Complete or handle issues
        }
    )
    
    workflow.add_edge("orchestrator", END)
    
    return workflow.compile()


if __name__ == "__main__":
    # Create and test the system
    translation_system = create_translation_system()

    simple_data = {
        "source_text": "Hello, how are you today?",
        "source_language": "en",
        "target_language": "es"
    }

    # Test translation
    initial_state = get_initial_translation_state(simple_data)

    result = translation_system.invoke(initial_state)
    print("Translation Result:", result["translated_text"])