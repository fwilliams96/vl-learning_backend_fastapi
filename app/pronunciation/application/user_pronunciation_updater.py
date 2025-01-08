
from app.pronunciation.domain.pronunciation import Pronunciation
from app.pronunciation.infrastructure.persistence.mongo_pronunciation_repository import MongoPronunciationRepository

class PronunciationUpdater:

    def __init__(self, 
                 pronunciation_repository = MongoPronunciationRepository()) -> None:
        self.pronunciation_repository = pronunciation_repository

    def update(self, pronunciation: Pronunciation) -> Pronunciation:
        return self.pronunciation_repository.update_pronunciation(pronunciation)