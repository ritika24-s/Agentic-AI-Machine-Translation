from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from apis.services.websocket import manager
import logging
import json
from datetime import datetime


router = APIRouter(tags=["websocket"])
logger = logging.getLogger(__name__)


@router.websocket("/ws/{request_id}")
async def websocket_endpoint(websocket: WebSocket, request_id: str):
    """
    WebSocket endpoint for real-time agent activity updates
    
    Frontend usage:
    ```javascript
    const ws = new WebSocket(`ws://localhost:8000/ws/${requestId}`);
    ws.onmessage = (event) => {
        const update = JSON.parse(event.data);
        // Handle agent activity updates
        console.log('Agent update:', update);
    };
    ```
    """
    await manager.connect(websocket, request_id)
    
    try:
        while True:
            # Keep connection alive and handle incoming messages
            message = await websocket.receive_text()
            
            # Handle client messages (optional)
            try:
                data = json.loads(message)
                
                if data.get("type") == "ping":
                    await manager.send_personal_message(websocket, {
                        "type": "pong",
                        "timestamp": datetime.now().isoformat()
                    })
                
            except json.JSONDecodeError:
                await manager.send_personal_message(websocket, {
                    "type": "error",
                    "message": "Invalid JSON message"
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"WebSocket disconnected for request {request_id}")
    except Exception as e:
        logger.error(f"WebSocket error for request {request_id}: {e}")
        manager.disconnect(websocket)


@router.websocket("/ws/system")
async def system_websocket(websocket: WebSocket):
    """
    System-wide WebSocket for general updates
    
    Use for:
    - System status updates
    - Agent health monitoring
    - Global announcements
    """
    await websocket.accept()
    
    try:
        # Send system status
        await websocket.send_text(json.dumps({
            "type": "system_status",
            "status": "connected",
            "agents_available": 5,
            "system_load": "normal"
        }))
        
        # Keep alive
        while True:
            await websocket.receive_text()
            
    except WebSocketDisconnect:
        logger.info("System WebSocket disconnected")