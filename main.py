from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import time
from Translator.translate_factory import TranslateFactory


app = Flask(__name__)
CORS(app)


@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    source_lang = data.get("source_lang", "auto")
    target_lang = data.get("target_lang", "es")
    language_model = data.get("language_model", "libretranslate")
    translate_factory = TranslateFactory()
    translate = translate_factory.get_translate(language_model)
    translated_text = translate.translate_text(data, source_lang, target_lang)
    translate.save_translated_text(translated_text, target_lang, data)
    return jsonify({
        'translation': translated_text.get('translatedText'),
        'confidence': translation_result.get('confidence', 0),
        'quality_metrics': quality_metrics,
        'agent_decision': make_agent_decision(quality_metrics)
    })


# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=5000)