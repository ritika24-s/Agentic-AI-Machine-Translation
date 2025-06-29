import json
import pandas as pd
import os

def read_json_file(file_path:str):
    """
    This function is used to read the file from the given path.
    
    Args:
        file_path (str): Path to the JSON file to be read
        
    Returns:
        pd.DataFrame: DataFrame containing the JSON data
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            df = pd.read_json(file)
            #  only select messages column if it exists
            df = df[["messages"]]
            print(df.head())
            return df
    except UnicodeDecodeError:
        # Fallback to latin-1 encoding if UTF-8 fails
        with open(file_path, "r", encoding="latin-1") as file:
            df = pd.read_json(file)
            df = df[["messages"]]
            print(df.head())
            return df
        
def get_data_to_app():
    """
    This function is used to get the data to the app.
    """
    # Load training data
    df = read_json_file("data/messages_train.json")
    return df



def map_json_to_translation_state(message_data: dict) -> dict:
    """Convert JSON structure to TranslationState format"""
    message = message_data["messages"][0] if message_data.get("messages") else {}
    
    return {
        "messages": [],
        "source_text": message.get("msg_o", message.get("msg", "")),
        "source_language": message.get("source_lang", "auto"), 
        "target_language": "es",  # or from request
        "translated_text": "",
        "confidence_score": 0.0,
        "conversation_context": [],
        "needs_human_review": False,
        "error_messages": [],
        # Add metadata for tracking
        "original_message_id": str(message_data.get("_id", {}).get("$oid", "")),
        "customer_name": message.get("name", ""),
        "timestamp": message.get("ts", {}).get("$date", "")
    }


def serialize_translation_result(result: dict) -> dict:
    """Convert LangGraph result to JSON-serializable format"""
    
    # Convert messages to simple strings
    messages = result.get("messages", [])
    serialized_messages = []
    
    for msg in messages:
        if hasattr(msg, 'content'):
            serialized_messages.append(msg.content)
        elif isinstance(msg, str):
            serialized_messages.append(msg)
        else:
            serialized_messages.append(str(msg))
    
    return {
        "success": True,
        "translation_summary": result.get("translation_summary", {}),
        "translated_text": result.get("translated_text", ""),
        "quality_score": result.get("quality_score", 0.0),
        "service_used": result.get("service_used", "unknown"),
        "needs_human_review": result.get("needs_human_review", False),
        "processing_messages": serialized_messages,
        "source_text": result.get("source_text", ""),
        "target_language": result.get("target_language", "")
    }