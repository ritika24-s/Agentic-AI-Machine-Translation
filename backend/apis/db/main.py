# Standard library imports
import logging
from typing import Dict, Any


def convert_message_to_dict(message: Any) -> Dict[str, Any]:
    """
    Convert a message object to a JSON-serializable dictionary.
    
    Args:
        message: The message object to convert
        
    Returns:
        Dict containing the message data in a JSON-serializable format
    """
    if hasattr(message, 'to_dict'):
        return message.to_dict()
    elif hasattr(message, '__dict__'):
        return {k: v for k, v in message.__dict__.items() 
                if not k.startswith('_')}
    elif isinstance(message, dict):
        return message
    else:
        return {"content": str(message)}


    
    
    
    
    