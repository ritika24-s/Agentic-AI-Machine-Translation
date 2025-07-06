#!/usr/bin/env python3
"""
Application Entry Point

Run this script to start the Agentic AI Translation System server.

Usage:
    python run.py
    
The server will start on http://localhost:8000
API documentation will be available at http://localhost:8000/docs
"""

import sys
import uvicorn
from pathlib import Path

# Add the current directory to Python path to ensure proper imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import the FastAPI app
from apis.main import app

if __name__ == "__main__":
    """
    Production-ready server configuration
    
    For development:
    - Auto-reload enabled
    - Single worker
    - Detailed logging
    
    For production, consider:
    - Multiple workers: --workers 4
    - Disable reload: --no-reload
    - Use gunicorn: gunicorn apis.main:app -w 4 -k uvicorn.workers.UvicornWorker
    """
    
    print("Starting Agentic AI Translation System...")
    print("API Documentation: http://localhost:8000/docs")
    print("Alternative Docs: http://localhost:8000/redoc")
    print("Health Check: http://localhost:8000/api/v1/health")
    print("WebSocket: ws://localhost:8000/ws")
    print()
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "apis.main:app",           # Module path to FastAPI app
            host="0.0.0.0",            # Listen on all interfaces  
            port=8000,                 # Port number
            reload=True,               # Auto-reload on code changes (dev mode)
            log_level="info",          # Logging level
            access_log=True,           # Log all HTTP requests
            reload_dirs=[str(current_dir)],  # Watch for changes in backend directory
            # Development settings
            workers=1,                 # Single worker for development
            # Add these for production:
            # workers=4,               # Multiple workers for production
            # reload=False,            # Disable auto-reload in production
        )
    except KeyboardInterrupt:
        print("\nServer stopped gracefully")
    except Exception as e:
        print(f"Failed to start server: {e}")
        sys.exit(1) 