class TranslateText:
    def translate_text(self, data, source_lang, target_lang):
        pass

    def save_translated_text(self, response_json:dict, target_language:str, data:dict):
        pass

    def speaker_identification(self, data:dict, no_of_people:int=2):
        """
        This function is used to return the respective speaker in the conversation.

        Args:
            data: dict: Contains the metadata of the text to be translated.
            no_of_people: int: Contains the number of people in the conversation.

        Returns:
            list: The respective speaker in the conversation.
        """
        return data.get("from", "agent")
    
    def calculate_quality_metrics(self, source_text:str, translated_text:str):
        self.confidence_score = self.quality_estimation.check_confidence_score(translated_text)
        self.length_difference = self.quality_estimation.length_difference(source_text, translated_text)

    def make_agent_decision(self, quality_metrics:dict)->str:
        """
        Return values allowed: approve/review/post-edit
        """
        if self.confidence_score >= 85 and self.length_difference <= 5:
            return "approve"
        elif self.confidence_score >= 65 and self.length_difference <= 10:
            return "post-edit"
        else:
            return "review"


class QualityEstimation:
    def length_difference(self, source_text:str, translated_text:str):
        return abs(len(source_text) - len(translated_text))
    
    def check_confidence_score(self, translated_text:dict)->int:
        """
        This function is used to return the confidence score of the translated text.

        Args:
            translated_text: dict: Contains the translated text and the confidence score.

        Returns:
            int: The confidence score.
        """
        return int(translated_text.get("confidence"))
    

class ConversationContextTracking:
    def __init__(self, conversation:dict):
        self.conversation = conversation

    def get_speaker(self, no_of_people:int=2):
        """
        This function is used to return the respective speaker in the conversation.

        Args:
            conversation: dict: Contains the conversation.

        Returns:
            list: The respective speaker in the conversation.
        """
        for message in self.conversation:
            if not message.get("from") and no_of_people == 2:
                message["from"] = "agent"
        return self.conversation
    
    def translation_consistency(self):
        """
        Check for translation consistency across turns
        """
        base_translation_language = self.conversation[0].get("target_language")
        for message in self.conversation:
            if message.get("target_language") != base_translation_language:
                return False
        return True

    def domain_detection(self):
        """
        This function is used to detect the domain of the conversation.
        """
        for message in self.conversation:
            if message.get("domain"):
                return message.get("domain")
        return "general"

