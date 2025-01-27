from fastapi import APIRouter, BackgroundTasks, HTTPException, Header, status

from app.pronunciation.application.pronunciation_analyzer import PronunciationAnalyzer
from app.pronunciation.application.pronunciation_finder import PronunciationFinder
from app.pronunciation.application.pronunciation_generator import PronunciationGenerator
from app.pronunciation.application.user_pronunciation_updater import PronunciationUpdater
from app.pronunciation.domain.pronunciation import Pronunciation, UserSpeech

router = APIRouter(prefix='/api/v1/pronunciations', tags=["pronunciations"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

@router.post('', response_model=Pronunciation, status_code=status.HTTP_200_OK)
def create_user_pronunciation(x_user_id: str = Header(None, alias="X-User-Id")):
    return PronunciationGenerator().generate()

@router.get('/{pronunciation_id}', response_model=Pronunciation, status_code=status.HTTP_200_OK)
def get_user_pronunciation(pronunciation_id: str):
    user_pronunciation = PronunciationFinder().find(pronunciation_id)
    if user_pronunciation == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pronunciation activity not found")
    return user_pronunciation

@router.post('/{pronunciation_id}/close', response_model=Pronunciation, status_code=status.HTTP_200_OK)
def close_user_pronunciation(pronunciation_id: str, user_speech: UserSpeech, background_tasks: BackgroundTasks):
    pronunciation = PronunciationFinder().find(pronunciation_id)
    if pronunciation == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pronunciation activity not found")
    
    pronunciation.user_speech = user_speech
    pronunciation = PronunciationAnalyzer().analize_pronunciation(pronunciation)

    pronunciation.id = pronunciation_id
    pronunciation.finished = True

    pronunciation = PronunciationUpdater().update(pronunciation)
    return pronunciation