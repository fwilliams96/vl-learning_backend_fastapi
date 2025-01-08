from app.shared.domain.external_speech_to_text_converter import ExternalSpeechToTextConverter
from app.shared.infrastructure.openai.openai_client import transcribe_audio_to_text

class WhisperSpeechToTextConverter(ExternalSpeechToTextConverter):
    def __init__(self) -> None:
        pass

    def transcribe(self, filename: str) -> str:
        with open(filename, "rb") as audio_file:
            return transcribe_audio_to_text(audio_file)