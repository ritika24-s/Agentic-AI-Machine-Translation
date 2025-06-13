import pandas as pd
import requests


def read_data(filename:str)->pd.DataFrame:
    with open(filename, "r", encoding="utf-8") as file:
        data = pd.read_json(file, orient="index", lines=True, nrows=10)
    return data

def translate(data:dict, target_language:str = "es")->dict:
    res = requests.post("https://libretranslate.com/translate", 
    {
        "q": data["value_o"] if data.get("value_o") else data["value"],
        "source": data.get("source_lang","auto"),
        "target": target_language,
    }, 
    headers={"Content-Type": "application/json"})
    return res.json()

def check_confidence_score(response_json):
    if response_json.get("confidence") < 50:
        return response_json["language"]
    return "try again"

    
def save_translated_text(response_json:dict, target_language:str, data:dict):
    if check_confidence_score(response_json["detectedLanguage"]) == "try again":
        data["translated_text"] = translate(data, target_language)
    else:
        data["translated_text"] = response_json["translatedText"]


if __name__ == "__main__":
    data = read_data("cxdb_5d42c72a9450811eb91d419a054c185c.messages.json")
    print(data.head())
