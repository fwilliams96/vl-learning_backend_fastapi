import abc

class ExternalTextToSpeechConverter(abc.ABC):

    @abc.abstractclassmethod
    def transform(self, text: str) -> bytes:
        pass