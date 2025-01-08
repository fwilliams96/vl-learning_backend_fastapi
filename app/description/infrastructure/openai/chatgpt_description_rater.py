from app.description.domain.description import DescriptionResult
from app.description.domain.external_description_rater import ExternalDescriptionRater
from app.shared.infrastructure.openai.openai_client import interpret_image
from app.shared.infrastructure.utils.utils import json_to_string, string_to_json

class ChatgptDescriptionRater(ExternalDescriptionRater):

    json_format = {
        "rating": "your description rating from 0 to 10", 
        "comments": "your improvement tips or your congratulations",
        "description": "your example of description"
    }

    description_rater_prompt = f"Rate the following description of the attached image from 0 to 10. The response should follow this JSON format: {json_to_string(json_format)}"
     
    def rate(self, user_description: str, image_url: str) -> DescriptionResult:
        messages= [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": ChatgptDescriptionRater.description_rater_prompt
                    },
                    {
                        "type": "text",
                        "text": user_description
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ]
        agent_response = interpret_image(messages)
        agent_response_json = string_to_json(agent_response)
        #print(agent_response_json)

        return DescriptionResult(
            rating=agent_response_json["rating"],
            solution=agent_response_json["description"],
            comments=agent_response_json["comments"]
        )
    

