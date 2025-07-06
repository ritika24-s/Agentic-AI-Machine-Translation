from langchain.chat_models import init_chat_model

class ModelSelector:
    """
    This class is used to select the model to use for the chatbot.
    """
    def get_model(self, model_type: str, model_name: str):
        print("Selected model: " + model_type + ":" + model_name)
        return init_chat_model(model_type + ":" + model_name)
    
llm = ModelSelector().get_model(model_type="groq", model_name="compound-beta")