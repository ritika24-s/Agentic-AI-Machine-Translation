import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Basic settings
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # API settings
    FASTAPI_PORT = int(os.getenv("FASTAPI_PORT", 8000))
    API_VERSION = os.getenv("API_VERSION", "v1")

    # rate limit settings
    RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", 60))
    RATE_LIMIT_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", 100))
    
    # Redis settings
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_TTL = int(os.getenv("REDIS_TTL", 3600))
    
    # Paths
    PROJECT_ROOT = Path(__file__).parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    LOGS_DIR = PROJECT_ROOT / "logs"
    
    def __init__(self):
        # Create necessary directories
        self.DATA_DIR.mkdir(exist_ok=True)
        self.LOGS_DIR.mkdir(exist_ok=True)

def get_env_var(var_name, default=None):
    """
    returns the value of the environment variable or the default value if not found
    """
    var_name = var_name.upper()
    if var_name in Config.__dict__:
        return Config.__dict__[var_name]
    else:
        raise ValueError(f"Environment variable {var_name} not found")


if __name__ == "__main__":
    print(get_env_var("ENVIRONMENT"))