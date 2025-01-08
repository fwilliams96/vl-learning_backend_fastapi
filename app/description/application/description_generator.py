import base64
import os
import time
import requests
from app.description.domain.description import Description, ImageDescription
from app.description.infrastructure.openai.chatgpt_image_generator import ChatgptImageGenerator
from app.description.infrastructure.persistence.mongo_description_repository import MongoDescriptionRepository
from app.shared.application.topic_generator import TopicGenerator
from app.shared.infrastructure.s3.aws_s3_client import upload_image_to_s3

class DescriptionGenerator:

    def __init__(self, 
                 topic_generator = TopicGenerator(), 
                 external_image_generator = ChatgptImageGenerator(),
                 description_repository = MongoDescriptionRepository()) -> None:
        self.topic_generator = topic_generator
        self.external_image_generator = external_image_generator
        self.description_repository = description_repository

    def generate(self) -> Description:
        topic = self.topic_generator.random_topic()

        image_url = self.external_image_generator.generate(topic)
        print(image_url)
        response = requests.get(image_url)
        image_bytes = response.content

        # Save image to tmp folder
        NANOts = time.time_ns() # generate to avoid clobber
        image_name = f"description_{NANOts}.jpg"
        image_path = f"/tmp/{image_name}.jpg"
        file_key = f'descriptions/{image_name}'
        with open(image_path, 'wb') as file:
            file.write(image_bytes)
        
        image_s3_url = upload_image_to_s3(image_path, file_key)

        # Eliminar el archivo temporal
        if os.path.exists(image_path):
            os.remove(image_path)
        
        image_description = ImageDescription(
            url=image_s3_url,
            topic=topic
        )
        image_description = self.description_repository.save_image_description(image_description)

        user_description = Description(
            topic=image_description.topic,
            finished=False,
            image_url=image_description.url,
            image_id=image_description.id
        )
        return self.description_repository.save_description(user_description)
