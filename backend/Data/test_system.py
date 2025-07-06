# test_system.py
import requests
import json

def test_with_your_sample_data():
    """Test with your actual JSON format"""
    
    sample_data = {
        "_id": {"$oid": "684edb23c9b311bf2e755b79"},
        "messages": [{
            "msg_o": "Guten Tag! Ich möchte mein Piano über ein Interface mit meinem Windows-PC verbinden.",
            "from": "customer",
            "name": "Lothar Simon",
            "source_lang": "de"
        }]
    }
    
    response = requests.post("http://localhost:5000/translate", json=sample_data)
    print("Response:", json.dumps(response.json(), indent=2))

def test_simple_translation():
    """Test with simple format"""
    
    simple_data = {
        "source_text": "Hello, how are you today?",
        "source_language": "en",
        "target_language": "es"
    }
    
    response = requests.post("http://localhost:5000/translate", json=simple_data)
    print("Simple test:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_simple_translation()
    test_with_your_sample_data()