from fastapi import APIRouter, BackgroundTasks, HTTPException, status

from app.listening.application.listening_checker import ListeningChecker
from app.listening.application.listening_creator import ListeningCreator
from app.listening.application.listening_finder import ListeningFinder
from app.listening.application.listening_generator import ListeningGenerator
from app.listening.application.listening_updater import ListeningUpdater
from app.listening.domain.listening import Listening


router = APIRouter(prefix='/listening', tags=["listening"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

@router.post('/', response_model=Listening, status_code=status.HTTP_200_OK)
async def create_listening(num_sentences: int):
    return ListeningGenerator().generate(num_sentences)

@router.get('/{user_listening_id}', response_model=Listening, status_code=status.HTTP_200_OK)
def get_user_listening(listening_id: str):
    listening = ListeningFinder().find(listening_id)
    if listening == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listening not found")
    return listening

@router.post('/{listening_id}/close', response_model=Listening, status_code=status.HTTP_200_OK)
def close_user_listening(listening_id: str, listening: Listening, background_tasks: BackgroundTasks):
    listening_db = ListeningFinder().find(listening_id)
    if listening_db == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listening not found")
    
    listening.id = listening_id
    listening.finished = True
    listening = ListeningUpdater().update(listening)
    return listening