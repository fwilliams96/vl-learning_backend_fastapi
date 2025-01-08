from typing import Optional
from bson import ObjectId
from app.listening.domain.listening import Listening
from app.listening.domain.listening_repository import ListeningRepository
from app.listening.infrastructure.persistence.mappers.domain_to_entity_mapper import map_domain_to_entity
from app.listening.infrastructure.persistence.mappers.entity_to_domain_mapper import map_entity_to_domain
from app.shared.infrastructure.persistence.config.mongo_config import db_client

class MongoListeningRepository(ListeningRepository):

    def save(self, listening: Listening):
        listening_db = map_domain_to_entity(listening)
        listening_id = db_client.listenings.insert_one(listening_db).inserted_id
        listening.id = str(listening_id)
        return listening
    
    def find(self, listening_id: str) -> Optional[Listening]:
        listening_db = db_client.listenings.find_one({"_id": ObjectId(listening_id)})
        return map_entity_to_domain(listening_db) if listening_db != None else None
    
    def update(self, listening: Listening) -> Listening:
        listening_db = map_domain_to_entity(listening)
        db_client.listenings.find_one_and_replace({"_id": ObjectId(listening.id)}, listening_db)
        return listening