import abc
from app.description.domain.description import DescriptionResult

class ExternalDescriptionRater(abc.ABC):

    @abc.abstractclassmethod
    def rate(self, user_description: str, image: str) -> DescriptionResult:
        pass