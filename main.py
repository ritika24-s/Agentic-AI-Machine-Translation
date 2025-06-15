from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import time
from Translator.translate_factory import TranslateFactory


app = Flask(__name__)
CORS(app)

@app.route("/translate", methods=["POST"])
def translate():
    """
    This api is used to translate the text.

    Args:
        data (dict): The data to be translated. It should contain the following keys:
            - source_text: str  # the source text to be translated
            - source_language: str  # the language of the source text
            - target_language: str  # the language to translate the source text to
            - language_model: str  # the language model to use for translation

    Returns:
        dict: The translated text.
    """
    data = request.json
    source_lang = data.get("source_language", "auto")
    target_lang = data.get("target_language", "es")
    language_model = data.get("language_model", "libretranslate")
    
    


# # Run the app
# if __name__ == "__main__":
#     app.run(debug=True, port=5000)

from Api.read_file import read_json_file


if __name__ == "__main__":
    df = read_json_file("data/messages_train.json")
    app.run(debug=True, port=5000)
    
    for index, row in df.iterrows():
        messages = row["messages"] if "messages" in row else []
        if not len(messages):
            continue

        # send messages to translate
        body = {
            "source_language": messages[0].get("source_lang", "auto"),
            "target_language": "es",
            "source_text": messages
        }
        response = requests.post("http://localhost:5000/translate", json=body)
        print(response.json())
