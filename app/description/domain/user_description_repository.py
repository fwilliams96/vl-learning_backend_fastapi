import abc
from typing import Optional
from app.description.domain.description import Description, ImageDescription

class DescriptionRepository(abc.ABC):

    @abc.abstractclassmethod
    def save_description(self, description: Description):
        pass

    @abc.abstractclassmethod
    def update_description(self, description: Description) -> Description:
        pass

    @abc.abstractclassmethod
    def find_description(self, description_id: str) -> Description:
        pass

    @abc.abstractclassmethod
    def save_image_description(self, image_description: ImageDescription) -> ImageDescription:
        pass

    @abc.abstractclassmethod
    def find_all_image_descriptions(self) -> list[ImageDescription]:
        pass

    @abc.abstractclassmethod
    def find_image_descriptions_by_topic(self, topic: str) -> list[ImageDescription]:
        pass
