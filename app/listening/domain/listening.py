from typing import Optional
from pydantic import BaseModel

class Word(BaseModel):
    word: str
    is_word: bool
    askable: bool
    wrong: bool = False
    
class Sentence(BaseModel):
    id: Optional[str] = None
    words: list[Word]
    sentence: str
    audio: str

class AudioSentence(Sentence):
    audio: str

class Listening(BaseModel):
    id: Optional[str] = None
    topic: str
    finished: bool = False
    sentences: list[Sentence] = []

class SentenceCheckResult(BaseModel):
    correct: bool
    correct_sentence: str