import requests
from fastapi import FastAPI

from apis.views import translate_request

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Hello World"}

@app.post("/translate")
async def translate(translation_request: TranslationRequest):
    req = await request.json()
    response = translate_request(req)
    if response.status_code == 200:
        return {
            "translated_text": response.json()["translated_text"],
            "status": response.json()["status"],
            "source_language": response.json()["source_language"],
            "target_language": response.json()["target_language"]
        }
    else:
        return {"error": "Failed to translate"}
