from typing import Optional
from bson import ObjectId
from app.pronunciation.domain.pronunciation import Pronunciation, Sentence, SentenceWord

def map_domain_to_entity(pronunciation: Pronunciation) -> dict:
    return {
        "topic": pronunciation.topic,
        "finished": pronunciation.finished,
        "sentence": map_sentence_domain_to_entity(pronunciation.sentence),
        "user_speech": get_user_speech(pronunciation),
        "routine_id": ObjectId(pronunciation.routine_id) if pronunciation.routine_id != None else None
    }

def get_user_speech(pronunciation: Pronunciation) -> dict:
    if pronunciation.user_speech != None:
        return {
            "audio": pronunciation.user_speech.audio    
        }
    return None

def map_sentence_domain_to_entity(pronunciation_sentence: Sentence) -> dict:
    return {
        "words": [map_sentence_word_domain_to_entity(word) for word in pronunciation_sentence.words],
        "sentence": pronunciation_sentence.sentence,
        "audio": pronunciation_sentence.audio
    }

def map_sentence_word_domain_to_entity(pronunciation_word: SentenceWord) -> dict:
    return {
        "word": pronunciation_word.word,
        "wrong": pronunciation_word.wrong,
        "is_word": pronunciation_word.is_word,
    }