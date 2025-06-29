from typing import Dict

def translate_request(request:Dict):
    """
    This function is used to check the type of request and call the appropriate function
    """
    if request["type"] == "text":
        return translate_text(request)
    elif request["type"] == "file":
        return translate_file(request)
    elif request["type"] == "batch":
        return translate_batch(request)
    else:
        raise ValueError("Invalid request type")

def translate_text(request:Dict):
    pass

def translate_file(request:Dict):
    pass

def translate_batch(request:Dict):
    pass
