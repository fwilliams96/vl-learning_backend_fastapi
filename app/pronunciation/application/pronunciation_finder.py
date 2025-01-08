from typing import Optional
from app.pronunciation.domain.pronunciation import Pronunciation
from app.pronunciation.infrastructure.persistence.mongo_pronunciation_repository import MongoPronunciationRepository

class PronunciationFinder:

    def __init__(self, pronunciation_repository = MongoPronunciationRepository()) -> None:
        self.pronunciation_repository = pronunciation_repository

    def find(self, pronunciation_id: str) -> Pronunciation:
        return self.pronunciation_repository.find_pronunciation(pronunciation_id)