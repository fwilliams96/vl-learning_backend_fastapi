import base64
import json
import subprocess
import time
from fastapi import APIRouter, HTTPException, status

from app.chat.domain.message import Message
from app.shared.infrastructure.openai.openai_client import get_prediction

router = APIRouter(prefix='/chat', tags=["chat"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

RHUBARB_PATH = "./bin/rhubarb"
FFMPG_PATH = "ffmpeg"  # Asegúrate de que ffmpeg esté instalado y accesible desde la terminal

ENGLISH_TEACHER_CONTEXT = '''
                You are a virtual English teacher.
                You will always reply with a JSON array of messages. With a maximum of 3 messages.
                Each message has a text, facialExpression, and animation property.
                The different facial expressions are: smile, sad, angry, surprised, funnyFace, and default.
                The different animations are: Talking_1, Talking_2, SalsaDancing, Laughing, Idle and Sad.
                '''

FUNNY_PERSON_CONTEXT = '''
                You are a funny person.
                You will always reply with a JSON array of messages. With a maximum of 3 messages.
                Each message has a text, facialExpression, and animation property.
                The different facial expressions are: smile, sad, angry, surprised, funnyFace, and default.
                The different animations are: Talking_1, Talking_2, SalsaDancing, Laughing, Idle and Sad.
                '''

@router.post('/chat')
async def chat(user_id: str, user_message: Message):
    print(user_message.content)
    ai_messages = get_ai_messages(user_message.content)

    response = []

    for ai_message in ai_messages:
        audio_name, mp3_audio_path = retrieve_agent_response_in_audio(ai_message["text"])

        wav_audio_path = f"audios/{audio_name}.wav"

        # Convertir el archivo a formato WAV utilizando ffmpeg
        ffmpeg_command = [
            FFMPG_PATH,
            "-i", mp3_audio_path,
            "-ac", "1",  # Mono channel
            "-ar", "44100",  # Sample rate 44.1 kHz
            wav_audio_path
        ]
        subprocess.run(ffmpeg_command, check=True)
        
        output_json_path = f"audios/{audio_name}.json"

        # Construir el comando de Rhubarb
        command = [
            RHUBARB_PATH,
            "-f", "json",
            "-o", output_json_path,
            wav_audio_path,
            "-r", "phonetic"
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error en Rhubarb: {result.stderr}")
            raise HTTPException(status_code=500, detail=f"Error en Rhubarb: {result.stderr}")
        
        # Leer el archivo JSON generado
        with open(output_json_path, "r") as json_file:
            json_data = json.load(json_file)

        audio_base64 = base64.b64encode(open(mp3_audio_path, "rb").read()).decode("utf-8")
        response.append({
            "text": ai_message["text"],
            "audio": audio_base64,
            "lipsync": json_data,
            "facialExpression": ai_message["facialExpression"],
            "animation": ai_message["animation"]
        })
       
    return response


def get_ai_messages(text: str):
    messages=[
        {
            "role": "system",
            "content": FUNNY_PERSON_CONTEXT,
        },
        {
            "role": "user", 
            "content": text
        }
    ]
    response = get_prediction(messages=messages, json_mode=True)
    response_json = json.loads(response)
    if response_json["messages"]:
        response_json = response_json["messages"];
    print(response_json)
    return response_json

def retrieve_agent_response_in_audio(text: str):
    audio_content = generate_audio(text)
    NANOts = time.time_ns() # generate to avoid clobber
    filename = f"audio_{NANOts}"
    audio_path = f"audios/{filename}.mp3"
# Guardar el archivo de audio recibido
    with open(audio_path, "wb") as audio_file:
        audio_file.write(audio_content)
    return filename, audio_path

def generate_audio(text: str):
    headers = {"xi-api-key": ELEVEN_API_KEY}
    body = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.50,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(
        f'{ELEVEN_API_URL}/v1/text-to-speech/{ELEVEN_VOICE_ID}', 
        headers=headers, json=body
    )
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al generar el audio con ElevenLabs")
    return response.content