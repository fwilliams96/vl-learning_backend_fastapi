from app.description.domain.description import Description, DescriptionResult, ImageDescription

def map_domain_to_entity(description: Description) -> dict:
    return {
        "topic": description.topic,
        "finished": description.finished,
        "image_url": description.image_url,
        "image_id": description.image_id,
        "user_description": description.user_description,
        "result": map_result_to_entity(description.result) if description.result != None else None
    }

def map_result_to_entity(result: DescriptionResult) -> dict:
    return {
        "solution": result.solution,
        "rating": result.rating,
        "comments": result.comments    
    }

def map_image_description_to_entity(image_description: ImageDescription) -> dict:
    return {
        "topic": image_description.topic,
        "url": image_description.url
    }