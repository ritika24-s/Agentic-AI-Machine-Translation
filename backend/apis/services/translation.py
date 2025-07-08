import asyncio
import logging
from typing import Dict, Any
from datetime import datetime

# Existing agent imports
from agent_architecture.agent_workflow import create_translation_system
from agent_architecture.States.translation_state import TranslationState, TranslationStateHelper

logger = logging.getLogger(__name__)


class AgentOrchestrationService:
    """Service layer for managing agent workflows"""
    
    def __init__(self):
        self.translation_system = create_translation_system()
        self.active_translations = {}  # Track ongoing translations
        
    async def execute_translation_workflow(
        self, 
        request_data: Dict[str, Any], 
        websocket_manager=None
    ) -> Dict[str, Any]:
        """
        Execute the full agent workflow with WebSocket updates
        
        Args:
            request_data: Translation request data
            websocket_manager: Optional WebSocket manager for real-time updates
        """
        request_id = request_data.get("request_id")
        
        try:
            # Store translation state for tracking
            self.active_translations[request_id] = {
                "status": "started",
                "start_time": datetime.now(),
                "current_agent": None
            }
            
            # Send initial status update
            if websocket_manager:
                await websocket_manager.send_agent_update(request_id, {
                    "type": "translation_started",
                    "agents": ["intelligence_router", "context_manager", "translation_specialist", 
                              "quality_guardian", "results_synthesizer"],
                    "current_agent": "intelligence_router",
                    "status": "analyzing_text"
                })
            
            # Create initial state for LangGraph
            initial_state = TranslationStateHelper.get_initial_translation_state(request_data)
            
            # Execute workflow with progress tracking
            result = await self._execute_with_progress_tracking(
                initial_state, request_id, websocket_manager
            )
            
            # Update final status
            self.active_translations[request_id]["status"] = "completed"
            
            if websocket_manager:
                await websocket_manager.send_agent_update(request_id, {
                    "type": "translation_completed",
                    "result": result,
                    "total_time": (datetime.now() - self.active_translations[request_id]["start_time"]).total_seconds()
                })
            
            return result
            
        except Exception as e:
            logger.error(f"Agent workflow failed for {request_id}: {str(e)}")
            
            if websocket_manager:
                await websocket_manager.send_agent_update(request_id, {
                    "type": "translation_failed",
                    "error": str(e)
                })
            
            # Clean up
            if request_id in self.active_translations:
                del self.active_translations[request_id]
            
            raise
    
    async def _execute_with_progress_tracking(
        self, 
        initial_state: TranslationState, 
        request_id: str,
        websocket_manager=None
    ) -> Dict[str, Any]:
        """Execute workflow with real-time progress updates"""
        
        # Since LangGraph runs synchronously, we run it in a thread
        # but we can still send periodic updates
        
        async def run_with_updates():
            # Start the workflow in a thread
            workflow_task = asyncio.create_task(
                asyncio.to_thread(self.translation_system.invoke, initial_state)
            )
            
            # Send periodic status updates while workflow runs
            agent_sequence = [
                ("intelligence_router", "Analyzing text complexity..."),
                ("context_manager", "Processing context..."),
                ("translation_specialist", "Translating text..."),
                ("quality_guardian", "Reviewing quality..."),
                ("results_synthesizer", "Finalizing results...")
            ]
            
            update_interval = 0.5  # Send updates every 500ms
            agent_index = 0
            
            while not workflow_task.done():
                if websocket_manager and agent_index < len(agent_sequence):
                    agent_name, status = agent_sequence[agent_index]
                    
                    self.active_translations[request_id]["current_agent"] = agent_name
                    
                    await websocket_manager.send_agent_update(request_id, {
                        "type": "agent_progress",
                        "current_agent": agent_name,
                        "status": status,
                        "progress": (agent_index + 1) / len(agent_sequence) * 100
                    })
                    
                    agent_index = min(agent_index + 1, len(agent_sequence) - 1)
                
                await asyncio.sleep(update_interval)
            
            return await workflow_task
        
        return await run_with_updates()
    
    def get_translation_status(self, request_id: str) -> Dict[str, Any]:
        """Get current status of a translation"""
        return self.active_translations.get(request_id, {"status": "not_found"})
    
    async def cancel_translation(self, request_id: str) -> bool:
        """Cancel an ongoing translation"""
        if request_id in self.active_translations:
            # Note: LangGraph doesn't have built-in cancellation,
            # so this is a placeholder for future implementation
            self.active_translations[request_id]["status"] = "cancelled"
            return True
        return False

# Global service instance
agent_service = AgentOrchestrationService()