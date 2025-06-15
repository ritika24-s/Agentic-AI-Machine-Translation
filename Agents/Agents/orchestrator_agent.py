"""
The Orchestrator coordinates the entire workflow and handles errors
Orchestration Responsibilities:
Memory management: Update translation memory and conversation context
Result formatting: Prepare user-friendly output with quality indicators
Error coordination: Handle failures and route to appropriate recovery strategies
"""
from Agents.States.translation_state import TranslationState


def orchestrator_agent(state: TranslationState) -> dict:
    """Coordinate workflow and handle final processing"""
    quality_score = state.get("quality_score", 0.0)
    quality_issues = state.get("quality_issues", [])
    translated_text = state["translated_text"]
    
    # Prepare final response
    if quality_score >= 0.6:
        # Acceptable translation
        final_status = "completed"
        output_text = translated_text
        
        # Update translation memory for future consistency
        translation_memory = state.get("translation_memory", {})
        translation_memory[state["current_text"]] = translated_text
        
        # Update conversation context
        conversation_context = state.get("conversation_context", [])
        conversation_context.append(f"Source: {state['current_text']} → Target: {translated_text}")
        
    else:
        # Quality issues detected
        final_status = "needs_review"
        output_text = f"Translation quality issues detected: {', '.join(quality_issues)}"
        translation_memory = state.get("translation_memory", {})
        conversation_context = state.get("conversation_context", [])
    
    # Generate summary for user
    service_used = state.get("service_used", "unknown")
    summary = {
        "translation": output_text,
        "quality_score": quality_score,
        "service_used": service_used,
        "status": final_status,
        "issues": quality_issues if quality_issues else None
    }
    
    return {
        "final_status": final_status,
        "translation_summary": summary,
        "translation_memory": translation_memory,
        "conversation_context": conversation_context[-10:],  # Keep last 10 for memory management
        "messages": [f"Orchestrator: {final_status} - Quality: {quality_score:.2f}"]
    }