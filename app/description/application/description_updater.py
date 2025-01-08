
from app.description.domain.description import Description
from app.description.infrastructure.persistence.mongo_description_repository import MongoDescriptionRepository


class DescriptionUpdater:

    def __init__(self, description_repository = MongoDescriptionRepository()) -> None:
        self.description_repository = description_repository

    def update(self, description: Description) -> Description:
        return self.description_repository.update_description(description)