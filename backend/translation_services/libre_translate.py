import requests
from Translator.base_translate import TranslateText
from monitoring.monitoring import setup_logging

logger = setup_logging(__name__)

class LibreTranslate(TranslateText):
    def __init__(self):
        self.base_url = "https://libretranslate.com/"
        self.headers = {"Content-Type": "application/json"}

    def translate_text(self, data:dict, source_language:str="auto", target_language:str="es"):
        translated_text = self.libre_translate(data, source_language, target_language)
        
        return {
        "source_language": source_language,
        "target_language": target_language,
        "source_text": data["value_o"] if data.get("value_o") else data["value"],
        'translated_text': translated_text.get('translatedText'),
        'confidence': translated_text.get('confidence', 0),
        'quality_metrics': self.calculate_quality_metrics(data["value_o"], translated_text.get('translatedText')),
        'agent_decision': self.make_agent_decision(self.calculate_quality_metrics(data["value_o"], translated_text.get('translatedText')))
        }
    
    def libre_translate(self, data:dict, source_language:str="auto", target_language:str="es", detect_language:bool=False):
        """
        This function is used to make a post request to the libretranslate api.
        The response json received from the api is then modified and returned.

        Sample response json returned by the api:
        {
            "detectedLanguage": { # this is when source language = "auto"
                "confidence": 83,
                "language": "it"
            },
            "translatedText": "Bye!" # this is the translated text
        }

        Args:
            data: dict: Contains the text to be translated and the source language.
            source_language: str: The source language of the text. Default is "auto".
            target_language: str: The target language of the text. Default is "es".

        Returns:
        """
        try:
            url = self.base_url + "translate"
            payload = {
                "q": data["value_o"] if data.get("value_o") else data["value"],
                "source": data.get("source_lang", source_language),
                "target": target_language,
            }
            res = requests.post(url,
                                payload,
                                headers=self.headers,
                                timeout=10)
            
            res.raise_for_status()  # Raise exception for bad status codes

            response_json = res.json()
            if detect_language:
                return response_json.get("detectedLanguage")
            else:
                return response_json.get("translatedText")

        except requests.exceptions.RequestException as e:
            logger.error(f"LibreTranslate API error: {str(e)}")
            return {"translatedText": "", "confidence": 0}
            
        except Exception as e:
            logger.error(f"Error in libre_translate: {e}")
            return {"translatedText": "", "confidence": 0}

        

    # def check_confidence_score(self, translated_text:dict):
    #     if translated_text.get("confidence") < 50:
    #         return translated_text.get("language")
    #     return "need review"
        
    def save_translated_text(self, response_json:dict, target_language:str, data:dict):
        if self.check_confidence_score(response_json["detectedLanguage"]) == "try again":
            data["translated_text"] = self.translate_text(data, target_language)
        else:
            data["translated_text"] = response_json["translatedText"]