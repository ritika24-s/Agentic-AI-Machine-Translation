from fastapi import Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)


class TranslationException(Exception):
    """Custom exception for translation errors"""
    def __init__(self, message: str, error_code: str = "TRANSLATION_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class AgentTimeoutException(TranslationException):
    """Exception for agent timeout"""
    def __init__(self, agent_name: str, timeout_seconds: int):
        message = f"Agent {agent_name} timed out after {timeout_seconds} seconds"
        super().__init__(message, "AGENT_TIMEOUT")

async def translation_exception_handler(request: Request, exc: TranslationException):
    """Handle custom translation exceptions"""
    logger.error(f"Translation error: {exc.message}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": exc.error_code,
            "detail": exc.message,
            "type": "translation_error"
        }
    )

async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "detail": "An unexpected error occurred",
            "type": "server_error"
        }
    )