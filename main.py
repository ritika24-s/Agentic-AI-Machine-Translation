# Standard library imports
import logging
from typing import Dict, Any, List, Union

# Third-party imports
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

# Local imports
from AgentArchitecture.States.translation_state import get_initial_translation_state
from AgentArchitecture.agent_workflow import create_translation_system
from Api.read_file import read_json_file, map_json_to_translation_state
from monitoring import setup_logging

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

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Setup logging
logger = setup_logging()

# Initialize the translation system once
translation_system = create_translation_system()

@app.route("/translate", methods=["POST"])
def translate():
    """
    Translate using the multi-agent LangGraph system
    """
    try:
        data = request.json
        
        # Handle different input formats
        if "messages" in data:
            # JSON format
            initial_state = map_json_to_translation_state(data)
        else:
            # Direct API format
            initial_state = get_initial_translation_state(data)
        
        # Run through the multi-agent system
        result = translation_system.invoke(initial_state)
        
        # Return structured response
        return jsonify({
            "success": True,
            "translation_summary": result.get("translation_summary", {}),
            "quality_score": result.get("quality_score", 0.0),
            "service_used": result.get("service_used", "unknown"),
            "needs_human_review": result.get("needs_human_review", False),
            "processing_messages": result.get("messages", [])
        })
        
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "translation": "Translation system error"
        }), 500


if __name__ == "__main__":
    # Load training data
    df = read_json_file("data/messages_train.json")
    
    # Start the Flask server
    app.run(debug=True, port=5000)
    
    # Process training data
    for index, row in df.iterrows()[:5]:  # Process first 5 rows for testing
        messages = row["messages"] if "messages" in row else []
        if not len(messages):
            continue
        for message in messages:
            # Convert message to JSON-serializable format
            message_dict = convert_message_to_dict(message)
            try:
                response = requests.post("http://localhost:5000/translate", json=message_dict)
                response.raise_for_status()  # Raise exception for bad status codes
                logger.info(f"Successfully processed message: {message_dict.get('content', '')[:50]}...")
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to process message: {str(e)}")
