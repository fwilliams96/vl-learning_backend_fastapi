import base64
import os
import time

from app.description.domain.description import UserDescription, DescriptionResult, UserDescriptionFormat
from app.description.infrastructure.openai.chatgpt_description_rater import ChatgptDescriptionRater
from app.shared.application.speech_to_text_converter import SpeechToTextConverter

class DescriptionRater:

    BACKEND_DOMAIN = os.environ.get("BACKEND_DOMAIN")
    IMAGES_FOLDER = os.path.join("static", "images")

    def __init__(self, 
                 external_description_rater = ChatgptDescriptionRater()
                 ) -> None:
        self.external_description_rater = external_description_rater

    def rate(self, user_description: str, image_url: str) -> DescriptionResult:
        return self.external_description_rater.rate(user_description, image_url)