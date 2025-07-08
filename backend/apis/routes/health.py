from fastapi import APIRouter
import psutil

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check():
    """Comprehensive health check"""
    
    health_status = {
        "status": "healthy",
        "services": {},
        "system": {}
    }
    
    # Check agent system
    try:
        from agent_architecture.agent_workflow import create_translation_system
        translation_system = create_translation_system()
        health_status["services"]["agents"] = "healthy"
    except Exception as e:
        health_status["services"]["agents"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    # System metrics
    health_status["system"] = {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent
    }
    
    return health_status