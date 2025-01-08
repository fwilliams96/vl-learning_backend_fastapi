import base64

from app.shared.infrastructure.elevenlabs.elevenlabs_text_to_speech_converter import ElevenlabsTextToSpeechConverter

class TextToSpeechConverter:

    def __init__(self, external_text_to_speech_converter = ElevenlabsTextToSpeechConverter()) -> None:
        self.external_text_to_speech_converter = external_text_to_speech_converter

    def transform(self, text: str) -> bytes:
        return self.external_text_to_speech_converter.transform(text)

    def transform_to_base64(self, text: str) -> str:
        speech_bytes = self.external_text_to_speech_converter.transform(text)
        return base64.b64encode(speech_bytes).decode('utf-8')