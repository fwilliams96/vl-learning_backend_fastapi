from app.listening.domain.listening import Listening
from app.listening.infrastructure.persistence.mongo_listening_repository import MongoListeningRepository

class ListeningUpdater:

    def __init__(self, 
                 listening_repository = MongoListeningRepository()) -> None:
        self.listening_repository = listening_repository

    def update(self, listening: Listening) -> Listening:
        return self.listening_repository.update(listening)