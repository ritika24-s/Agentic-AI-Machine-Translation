# apis/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
import logging

# Import all your routes
from apis.routes import translation, documents, websocket, health
from apis.utils.exceptions import (
    translation_exception_handler, 
    global_exception_handler,
    TranslationException
)
from apis.middleware.rate_limit import RateLimitMiddleware
from apis.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Agentic AI Translation System")
    
    # Initialize services
    try:
        from agent_architecture.agent_workflow import create_translation_system
        translation_system = create_translation_system()
        logger.info("Agent system initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize agent system: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Agentic AI Translation System")


# Create FastAPI application instance with metadata
app = FastAPI(
    title="Agentic AI Translation System",
    description="Multi-agent translation system with 5 specialized AI agents",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",  # Interactive API documentation
    redoc_url="/redoc"  # Alternative API documentation
)

# CORS middleware enables Next.js frontend to make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,  # Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting
app.add_middleware(RateLimitMiddleware, requests_per_minute=60)

# Add exception handlers
app.add_exception_handler(TranslationException, translation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Include routers
app.include_router(translation.router)
app.include_router(documents.router)
app.include_router(websocket.router)
app.include_router(health.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Agentic AI Translation System",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)