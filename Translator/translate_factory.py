from Translator.base_translate import TranslateText
from Translator.google_translate import GoogleTranslate
from Translator.libre_translate import LibreTranslate
from Translator.deepl_translate import DeeplTranslate



class TranslateFactory:
    def get_translate(self, translate_type:str)->TranslateText:
        if translate_type == "google":
            return GoogleTranslate()
        elif translate_type == "libretranslate  ":
            return LibreTranslate()
        elif translate_type == "deepl":
            return DeeplTranslate()