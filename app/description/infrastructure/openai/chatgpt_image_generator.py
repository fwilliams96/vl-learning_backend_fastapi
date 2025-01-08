from app.description.domain.external_image_generator import ExternalImageGenerator
from app.shared.infrastructure.openai.openai_client import generate_image

class ChatgptImageGenerator(ExternalImageGenerator):

    image_generator_prompt = lambda topic: f"Generate a describable image based on the following topic: {topic}"
     
    def generate(self, topic: str) -> str:
        return generate_image(ChatgptImageGenerator.image_generator_prompt(topic))
    

