import abc
from typing import Optional
from app.pronunciation.domain.pronunciation import Pronunciation

class PronunciationRepository(abc.ABC):

    @abc.abstractclassmethod
    def save_pronunciation(self, pronunciation: Pronunciation):
        pass

    @abc.abstractclassmethod
    def update_pronunciation(self, pronunciation: Pronunciation) -> Pronunciation:
        pass

    @abc.abstractclassmethod
    def find_pronunciation(self, pronunciation_id: str) -> Pronunciation:
        pass