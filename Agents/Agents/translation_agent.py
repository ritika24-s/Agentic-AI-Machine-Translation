"""
The Translation Agent performs the core translation work using free services
"""

from Agents.States.translation_state import TranslationState
from Translator.translate_factory import TranslateFactory

def translate_libretranslate(source_text: str, source_language: str="auto", target_language: str="es") -> tuple[str, float]:
    """
    Function to instantiate LibreTranslate object and translate text using libretranslate
    """
    libre_translate = TranslateFactory().get_translate("libretranslate")
    translated_text, confidence = libre_translate.translate_text(source_text, source_language, target_language)
    return translated_text, confidence

def translation_agent(translation_state: TranslationState) -> dict:
    """
    Perform the core translation work using free services
    Args:
        translation_state (TranslationState): The current state of the translation process

    Returns:
        dict: A dictionary containing the translated text
    """
    source_text = translation_state["source_text"]
    source_language = translation_state.get("source_language", "auto")
    target_language = translation_state.get("target_language", "es")

    approach = translation_state.get("translation_approach", "direct_translation")
    
    translation_result = None
    confidence_score = 0.0
    service_used = None

    # create instances of translation service
    libre_translate_result, libre_confidence = translate_libretranslate(source_text, source_language, target_language)
    # google_translate_result, google_confidence = translate_google(source_text, source_language, target_language)
    # deepl_translate_result, deepl_confidence = translate_deepl(source_text, source_language, target_language)
    # huggingface_translate_result, huggingface_confidence = translate_huggingface(source_text, source_language, target_language)

    if libre_confidence > max(libre_confidence, confidence_score):
        confidence_score = libre_confidence
        service_used = "libretranslate"
        translation_result = libre_translate_result
    else:
        confidence_score = 0.0
        service_used = None

    # Apply translation approach adjustments
    if approach == "terminology_focused" and translation_result:
        translation_result = apply_terminology_consistency(
            translation_result, translation_state.get("repeated_phrases", [])
        )
        confidence_score += 0.1  # Boost confidence for terminology consistency

    return {
        "translated_text": translation_result or "Translation failed",
        "confidence_score": confidence_score,
        "service_used": service_used,
        "messages": [f"Translation: {service_used} produced result with {confidence_score:.2f} confidence"]
    }

def apply_terminology_consistency(translation: str, repeated_phrases: list) -> str:
    """Ensure consistent translation of repeated terms"""
    for original, consistent_translation in repeated_phrases:
        # Simple replacement - in production, use more sophisticated matching
        translation = translation.replace(original, consistent_translation)
    return translation