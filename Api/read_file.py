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


