from typing import Optional
from bson import ObjectId
from app.description.domain.description import Description, ImageDescription
from app.description.domain.user_description_repository import DescriptionRepository
from app.description.infrastructure.persistence.mappers.domain_to_entity_mapper import map_domain_to_entity, map_image_description_to_entity
from app.description.infrastructure.persistence.mappers.entity_to_domain_mapper import map_entity_to_domain, map_image_description_to_domain
from app.shared.infrastructure.persistence.config.mongo_config import db_client

class MongoDescriptionRepository(DescriptionRepository):

    def save_description(self, description: Description) -> Description:
        description_db = map_domain_to_entity(description)
        description_id = db_client.descriptions.insert_one(description_db).inserted_id
        description.id = str(description_id)
        return description
    
    def update_description(self, description: Description) -> Description:
        description_db = map_domain_to_entity(description)
        db_client.descriptions.find_one_and_replace({"_id": ObjectId(description.id)}, description_db)
        return description
    
    def find_description(self, description_id: str) -> Optional[Description]:
        description_db = db_client.descriptions.find_one({"_id": ObjectId(description_id)})
        return map_entity_to_domain(description_db) if description_db != None else None
    
    def save_image_description(self, image_description: ImageDescription) -> ImageDescription:
        image_description_db = map_image_description_to_entity(image_description)
        image_description_id = db_client.image_descriptions.insert_one(image_description_db).inserted_id
        image_description.id = str(image_description_id)
        return image_description
    
    def find_all_image_descriptions(self) -> list[ImageDescription]:
        image_descriptions_db = db_client.image_descriptions.find()
        return [map_image_description_to_domain(image_description_db) for image_description_db in image_descriptions_db]
    
    def find_image_descriptions_by_topic(self, topic: str) -> list[ImageDescription]:
        image_descriptions_db = db_client.image_descriptions.find({"topic": topic})
        return [map_image_description_to_domain(image_description_db) for image_description_db in image_descriptions_db]