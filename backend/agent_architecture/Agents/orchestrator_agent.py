"""
The Orchestrator coordinates the entire workflow and handles errors
Orchestration Responsibilities:
Memory management: Update translation memory and conversation context
Result formatting: Prepare user-friendly output with quality indicators
Error coordination: Handle failures and route to appropriate recovery strategies

Role: The "Project Manager" - coordinates final output and drives continuous improvement.

Output Coordination:
- Confidence Scoring: Provides reliability indicators for each translation
- Alternative Suggestions: When multiple valid translations exist
- Explanation Generation: Why certain translation choices were made
- Improvement Recommendations: How to get better results next time

Continuous Learning Engine:
- Feedback Integration: Learns from user corrections and preferences
- Performance Analytics: Tracks which agent combinations work best for different content
- Pattern Recognition: Identifies recurring translation challenges
- Strategy Optimization: Adjusts routing and processing strategies over time

Business Intelligence:
- Usage Analytics: Which languages/domains are most requested
- Quality Trends: Are translations getting better over time?
- Cost Optimization: Which service combinations provide best value
- Scalability Insights: When to upgrade services or add capacity
"""
from agent_architecture.States.translation_state import TranslationState


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
        translation_memory[state["source_text"]] = translated_text
        
        # Update conversation context
        conversation_context = state.get("conversation_context", [])
        conversation_context.append(f"Source: {state['source_text']} → Target: {translated_text}")
        
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