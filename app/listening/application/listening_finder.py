from typing import Optional
from app.listening.domain.listening import Listening
from app.listening.infrastructure.persistence.mongo_listening_repository import MongoListeningRepository

class ListeningFinder:

    def __init__(self, listening_repository = MongoListeningRepository()) -> None:
        self.listening_repository = listening_repository

    def find(self, listening_id: str) -> Optional[Listening]:
        return self.listening_repository.find(listening_id)