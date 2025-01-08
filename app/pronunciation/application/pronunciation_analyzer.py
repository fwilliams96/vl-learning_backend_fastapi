import re
import string
from app.pronunciation.domain.pronunciation import Pronunciation, SentenceWord
from app.shared.application.speech_to_text_converter import SpeechToTextConverter

class PronunciationAnalyzer:

    def __init__(self, speech_to_text_converter = SpeechToTextConverter()) -> None:
        self.speech_to_text_converter = speech_to_text_converter

    def analize_pronunciation(self, pronunciation: Pronunciation) -> Pronunciation:

        transcription = self.speech_to_text_converter.transcribe(pronunciation.user_speech.audio)

        #print(f"Transcription of pronunciation: {transcription}")

        user_words = self.generate_words(transcription)
        user_words_dict = self.build_words_dict(user_words)
        ##print(f"User words: {user_words}")
        ##print(f"User words length: {len(user_words)}")

        words = [system_word for system_word in pronunciation.sentence.words if system_word.is_word == True]
        ##print(f"System words: {words}")
        ##print(f"System words length: {len(words)}")
        
        for word in pronunciation.sentence.words:
            if word.is_word and word.word not in user_words_dict:
                word.wrong = True
            else:
                word.wrong = False

        ##print(f"Words after analysis: {user_pronunciation.sentence.words}")
        return pronunciation
    
    def generate_words(self, sentence: str) -> list[SentenceWord]:

        # Agregamos espacios antes y después de cada signo de puntuación
        sentence_with_spaces = re.sub("([.,!?;])", r' \1 ', sentence)

        elements = sentence_with_spaces.split()

        # Creamos una lista de diccionarios, donde cada diccionario representa un elemento
        # y tiene un indicador de si es una palabra (no un signo de puntuación).
        elements_with_indicators = [
            {'word': element, 'is_word': True, 'wrong': False}
            for element in elements
            if element not in string.punctuation
        ]

        return [SentenceWord(**element) for element in elements_with_indicators]
    
    def build_words_dict(self, words: list[SentenceWord]) -> dict:
        words_dict = {}
        for word in words:
            words_dict[word.word] = True
        return words_dict
