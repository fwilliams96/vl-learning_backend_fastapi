from typing import Optional
from app.description.domain.description import Description
from app.description.infrastructure.persistence.mongo_description_repository import MongoDescriptionRepository

class DescriptionFinder:

    def __init__(self, description_repository = MongoDescriptionRepository()) -> None:
        self.description_repository = description_repository

    def find(self, description_id: str) -> Optional[Description]:
        return self.description_repository.find_description(description_id)