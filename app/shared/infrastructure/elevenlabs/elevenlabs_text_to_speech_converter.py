from app.shared.domain.external_text_to_speech_converter import ExternalTextToSpeechConverter
from app.shared.infrastructure.elevenlabs.client.elevenlabs_client import text_to_speech

class ElevenlabsTextToSpeechConverter(ExternalTextToSpeechConverter):

    def transform(self, text: str) -> bytes:
        return text_to_speech(text)