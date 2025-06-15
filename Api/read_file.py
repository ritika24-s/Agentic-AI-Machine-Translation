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