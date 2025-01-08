import re
import string
from app.pronunciation.domain.pronunciation import Pronunciation, Sentence, SentenceWord
from app.pronunciation.infrastructure.openai.chatgpt_sentence_generator import ChatgptSentenceGenerator
from app.pronunciation.infrastructure.persistence.mongo_pronunciation_repository import MongoPronunciationRepository
from app.shared.application.topic_generator import TopicGenerator
from app.shared.application.text_to_speech_converter import TextToSpeechConverter

class PronunciationGenerator:

    def __init__(self, 
                 topic_generator = TopicGenerator(), 
                 external_sentence_generator = ChatgptSentenceGenerator(),
                 pronunciation_repository = MongoPronunciationRepository(),
                 text_to_speech = TextToSpeechConverter()) -> None:
        self.topic_generator = topic_generator
        self.external_sentence_generator = external_sentence_generator
        self.pronunciation_repository = pronunciation_repository
        self.text_to_speech = text_to_speech

    def generate(self) -> Pronunciation:
        topic = self.topic_generator.random_topic()

        sentence = self.external_sentence_generator.generate(topic)

        sentence = Sentence(
            sentence=sentence,
            audio=self.text_to_speech.transform_to_base64(sentence),
            words=self.generate_words(sentence)
        )

        pronunciation = Pronunciation(
            topic=topic,
            sentence=sentence
        )
        return self.pronunciation_repository.save_pronunciation(pronunciation)
    
    def generate_words(self, sentence: str) -> list[SentenceWord]:

        # Agregamos espacios antes y después de cada signo de puntuación
        sentence_with_spaces = re.sub("([.,!?;])", r' \1 ', sentence)

        elements = sentence_with_spaces.split()

        # Creamos una lista de diccionarios, donde cada diccionario representa un elemento
        # y tiene un indicador de si es una palabra (no un signo de puntuación).
        elements_with_indicators = [
            {'word': element, 'is_word': element not in string.punctuation, 'wrong': False}
            for element in elements
        ]

        return [SentenceWord(**element) for element in elements_with_indicators]