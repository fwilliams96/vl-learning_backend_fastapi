import random
import re
import string
from app.shared.application.text_to_speech_converter import TextToSpeechConverter
from app.shared.application.topic_generator import TopicGenerator
from app.listening.domain.listening import Listening, Sentence, Word
from app.listening.infrastructure.persistence.mongo_listening_repository import MongoListeningRepository
from app.pronunciation.infrastructure.openai.chatgpt_sentence_generator import ChatgptSentenceGenerator

class ListeningGenerator:

    def __init__(self, 
                 topic_generator = TopicGenerator(), 
                 external_sentence_generator = ChatgptSentenceGenerator(),
                 listening_repository = MongoListeningRepository(),
                 text_to_speech = TextToSpeechConverter()) -> None:
        self.topic_generator = topic_generator
        self.external_sentence_generator = external_sentence_generator
        self.listening_repository = listening_repository
        self.text_to_speech = text_to_speech

    def generate(self, num_sentences: int, routine_id = None) -> Listening:
        topic = self.topic_generator.random_topic()
        sentences = [{}]*num_sentences
        for num_sentence in range(num_sentences):
            sentence = self.external_sentence_generator.generate(topic)

            user_sentence = Sentence(
                sentence=sentence,
                audio=self.text_to_speech.transform_to_base64(sentence),
                words=self.generate_words(sentence)
            )

            #print(f"Audio sentence: {user_sentence.audio}")

            sentences[num_sentence] = user_sentence

        listening = Listening(
            topic=topic,
            sentences=sentences
        )
        return self.listening_repository.save(listening)
    
    def generate_words(self, sentence: str) -> list[Word]:

        # Agregamos espacios antes y después de cada signo de puntuación
        sentence_with_spaces = re.sub("([.,!?;])", r' \1 ', sentence)

        elements = sentence_with_spaces.split()

        # Creamos una lista de diccionarios, donde cada diccionario representa un elemento
        # y tiene un indicador de si es una palabra (no un signo de puntuación).
        elements_with_indicators = [
            {'word': element, 'is_word': element not in string.punctuation, 'wrong': False}
            for element in elements
        ]

        # Aquí seleccionamos aleatoriamente palabras para preguntar al usuario.
        words = [elemento for elemento in elements_with_indicators if elemento['is_word']]
        num_words_to_ask = max(1, len(words) // 5)

        question_indexes = random.sample(range(len(words)), num_words_to_ask)

        words_picked = [word['word'] for i, word in enumerate(words) if i in question_indexes]
        
        # Agregamos el indicador de pregunta a los elementos que son palabras.
        for element in elements_with_indicators:
            if element['is_word']:
                element['askable'] = element['word'] in words_picked
            else:
                element['askable'] = False

        return [Word(**element) for element in elements_with_indicators]