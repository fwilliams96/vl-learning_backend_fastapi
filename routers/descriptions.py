from fastapi import APIRouter, BackgroundTasks, HTTPException, Header, status

from app.description.application.description_finder import DescriptionFinder
from app.description.application.description_generator import DescriptionGenerator
from app.description.application.description_rater import DescriptionRater
from app.description.application.description_updater import DescriptionUpdater
from app.description.domain.description import Description, DescriptionResult, UserDescription, UserDescriptionFormat
from app.shared.application.speech_to_text_converter import SpeechToTextConverter

router = APIRouter(prefix='/api/v1/descriptions', tags=["descriptions"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

@router.post('', response_model=Description, status_code=status.HTTP_200_OK)
def create_user_description(x_user_id: str = Header(None, alias="X-User-Id")):
    return DescriptionGenerator().generate()

@router.get('/{user_description_id}', response_model=Description, status_code=status.HTTP_200_OK)
def get_user_description(user_description_id: str):
    description = DescriptionFinder().find(user_description_id)
    if description == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Description not found")
    return description

@router.post('/{user_description_id}/result', response_model=DescriptionResult, status_code=status.HTTP_200_OK)
def get_description_result(user_description_id: str, user_description: UserDescription, background_tasks: BackgroundTasks):
    description = DescriptionFinder().find(user_description_id)
    if description == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Description not found")
    
    user_description_content = user_description.content
    if user_description.format == UserDescriptionFormat.AUDIO:
        speech_to_text_converter = SpeechToTextConverter()
        user_description_content = speech_to_text_converter.transcribe(user_description.content)

    description_result = DescriptionRater().rate(user_description_content, description.image_url)
    description.result = description_result
    description.user_description = user_description_content
    description.id = user_description_id
    description.finished = True
    description = DescriptionUpdater().update(description)
    return description.result