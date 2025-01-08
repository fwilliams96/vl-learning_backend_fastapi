import abc

class ExternalSpeechToTextConverter(abc.ABC):

    @abc.abstractclassmethod
    def transcribe(self, filename: str) -> str:
        pass