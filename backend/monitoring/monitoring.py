# Standard library imports
import logging
from datetime import datetime
from typing import Dict, Any

def setup_logging():
    """Setup comprehensive logging for the translation system"""
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('translation_system.log'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def log_translation_request(data: Dict[str, Any], result: Dict[str, Any]):
    """Log translation requests for analysis"""
    
    logger = setup_logging()
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "source_text_length": len(data.get("source_text", "")),
        "source_language": data.get("source_language"),
        "target_language": data.get("target_language"), 
        "translation_success": result.get("success", False),
        "quality_score": result.get("quality_score", 0.0),
        "service_used": result.get("service_used"),
        "needs_human_review": result.get("needs_human_review", False)
    }
    
    logger.info(f"Translation request: {log_entry}")