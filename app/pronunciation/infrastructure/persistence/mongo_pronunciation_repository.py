from typing import Optional
from bson import ObjectId
from app.pronunciation.domain.pronunciation import Pronunciation
from app.pronunciation.domain.pronunciation_repository import PronunciationRepository
from app.pronunciation.infrastructure.persistence.mappers.domain_to_entity_mapper import map_domain_to_entity
from app.pronunciation.infrastructure.persistence.mappers.entity_to_domain_mapper import map_entity_to_domain
from app.shared.infrastructure.persistence.config.mongo_config import db_client

class MongoPronunciationRepository(PronunciationRepository):

    def save_pronunciation(self, pronunciation: Pronunciation) -> Pronunciation:
        pronunciation_db = map_domain_to_entity(pronunciation)
        pronunciation_id = db_client.pronunciation.insert_one(pronunciation_db).inserted_id
        pronunciation.id = str(pronunciation_id)
        return pronunciation
    
    def update_pronunciation(self, pronunciation: Pronunciation) -> Pronunciation:
        pronunciation_db = map_domain_to_entity(pronunciation)
        db_client.pronunciation.find_one_and_replace({"_id": ObjectId(pronunciation.id)}, pronunciation_db)
        return pronunciation
    
    def find_pronunciation(self, pronunciation_id: str) -> Pronunciation:
        user_pronunciation_db = db_client.pronunciation.find_one({"_id": ObjectId(pronunciation_id)})
        return map_entity_to_domain(user_pronunciation_db) if user_pronunciation_db != None else None