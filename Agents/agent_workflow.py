"""
System Benefits:

Intelligent routing: Different strategies for different text types
Quality assurance: Automatic retry loops and human escalation
Context awareness: Maintains consistency across conversations
Error resilience: Multiple fallback strategies prevent failures
"""
from langgraph.graph import StateGraph, START, END
from Agents.States.translation_state import TranslationState
from Agents.Agents.router_agent import router_agent
from Agents.Agents.context_manager_agent import context_manager_agent
from Agents.Agents.translation_agent import translation_agent
from Agents.Agents.qa_agent import qa_agent
from Agents.Agents.orchestrator_agent import orchestrator_agent
from Agents.States.conversation_state import ConversationState


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
    
    # Add all agents
    workflow.add_node("router", router_agent)
    workflow.add_node("context_manager", context_manager_agent)
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

# Create and test the system
translation_system = create_translation_system()

# Test translation
initial_state = {
    "messages": [],
    "current_text": "Hello, how are you today?",
    "target_language": "es",
    "conversation_context": [],
    "translation_memory": {}
}

result = translation_system.invoke(initial_state)
print("Translation Result:", result["translation_summary"])