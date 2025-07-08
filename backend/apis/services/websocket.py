from fastapi import WebSocket
from typing import Dict, List, Any
import json
import logging
from datetime import datetime


logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages WebSocket connections for real-time agent updates"""
    
    def __init__(self):
        # Active connections by request_id
        self.active_connections: Dict[str, List[WebSocket]] = {}
        # Connection metadata
        self.connection_metadata: Dict[WebSocket, Dict[str, Any]] = {}
    
    async def connect(self, websocket: WebSocket, request_id: str):
        """Accept new WebSocket connection and associate with request"""
        await websocket.accept()
        
        if request_id not in self.active_connections:
            self.active_connections[request_id] = []
        
        self.active_connections[request_id].append(websocket)
        self.connection_metadata[websocket] = {
            "request_id": request_id,
            "connected_at": datetime.now()
        }
        
        logger.info(f"WebSocket connected for request {request_id}")
        
        # Send initial connection confirmation
        await self.send_personal_message(websocket, {
            "type": "connection_established",
            "request_id": request_id,
            "message": "Connected to agent activity stream"
        })
    
    def disconnect(self, websocket: WebSocket):
        """Clean up disconnected WebSocket"""
        metadata = self.connection_metadata.get(websocket)
        if metadata:
            request_id = metadata["request_id"]
            
            if request_id in self.active_connections:
                self.active_connections[request_id].remove(websocket)
                
                # Clean up empty request groups
                if not self.active_connections[request_id]:
                    del self.active_connections[request_id]
            
            del self.connection_metadata[websocket]
            logger.info(f"WebSocket disconnected for request {request_id}")
    
    async def send_personal_message(self, websocket: WebSocket, message: Dict[str, Any]):
        """Send message to specific WebSocket connection"""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Failed to send WebSocket message: {e}")
            self.disconnect(websocket)
    
    async def send_agent_update(self, request_id: str, update: Dict[str, Any]):
        """Send agent activity update to all connections for a request"""
        if request_id not in self.active_connections:
            return
        
        message = {
            "type": "agent_update",
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            **update
        }
        
        # Send to all connections for this request
        disconnected_connections = []
        
        for websocket in self.active_connections[request_id]:
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Failed to send agent update: {e}")
                disconnected_connections.append(websocket)
        
        # Clean up failed connections
        for websocket in disconnected_connections:
            self.disconnect(websocket)
    
    async def broadcast_system_message(self, message: Dict[str, Any]):
        """Broadcast message to all connected clients"""
        system_message = {
            "type": "system_broadcast",
            "timestamp": datetime.now().isoformat(),
            **message
        }
        
        all_connections = []
        for connections in self.active_connections.values():
            all_connections.extend(connections)
        
        disconnected_connections = []
        
        for websocket in all_connections:
            try:
                await websocket.send_text(json.dumps(system_message))
            except Exception as e:
                logger.error(f"Failed to broadcast message: {e}")
                disconnected_connections.append(websocket)
        
        # Clean up failed connections
        for websocket in disconnected_connections:
            self.disconnect(websocket)


# Global connection manager instance
manager = ConnectionManager()