import abc
from typing import Optional
from app.listening.domain.listening import Listening

class ListeningRepository(abc.ABC):

    @abc.abstractclassmethod
    def save(self, listening: Listening) -> Listening:
        pass

    @abc.abstractclassmethod
    def find(self, listening_id: str) -> Optional[Listening]:
        pass

    @abc.abstractclassmethod
    def update(self, listening: Listening) -> Listening:
        pass