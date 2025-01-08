from fastapi import HTTPException
import requests
from app.shared.infrastructure.elevenlabs.client.config.elevenlabs_config import API_KEY

URL = "https://api.elevenlabs.io"
#ELEVEN_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"
#ELEVEN_VOICE_ID = "UQ5IbejUipji5H5NGGS0" #Fran
VOICE_ID = "letlmoMovQ02JuDYh3CW" #FWM

def text_to_speech(text: str) -> bytes:
    headers = {"xi-api-key": API_KEY}
    body = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.50,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(
        f'{URL}/v1/text-to-speech/{VOICE_ID}', 
        headers=headers, json=body
    )
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al generar el audio con ElevenLabs")
    return response.content