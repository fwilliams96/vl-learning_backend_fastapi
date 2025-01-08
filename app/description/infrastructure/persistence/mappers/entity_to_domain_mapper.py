from app.description.domain.description import Description, DescriptionResult, ImageDescription

def map_entity_to_domain(user_description: dict) -> Description:

    return Description(
        id=str(user_description["_id"]),
        topic=user_description["topic"],
        finished=user_description["finished"],
        image_url=user_description["image_url"],
        image_id=user_description["image_id"],
        user_description=user_description["user_description"],
        result=map_result_to_domain(user_description["result"]) if user_description["result"] != None else None
    )

def map_result_to_domain(result: dict) -> DescriptionResult:
    return DescriptionResult(
        comments=result["comments"],
        rating=result["rating"],
        solution=result["solution"]
    )

def map_image_description_to_domain(image_description: dict) -> ImageDescription:
    return ImageDescription(
        id=str(image_description["_id"]),
        url=image_description["url"],
        topic=image_description["topic"]
    )