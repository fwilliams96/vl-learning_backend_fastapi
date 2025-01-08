import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
import boto3
from openai import OpenAI
from app.chat.domain.message import Message
from fastapi.middleware.cors import CORSMiddleware

from routers.chat import router as chat_router
from routers.listening import router as listenings_router
from routers.pronunciation import router as pronunciations_router
from routers.description import router as descriptions_router
#from routers.images import router as images_router
#from routers.role_play import router as role_play_router

client = OpenAI()
app = FastAPI()

# Define cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(chat_router)
app.include_router(listenings_router)
app.include_router(pronunciations_router)
app.include_router(descriptions_router)
#app.include_router(images.router)
#app.include_router(role_play.router)

# El cliente de boto3 utilizará automáticamente el IAM Role asignado
s3 = boto3.client("s3", region_name="eu-central-1")  # Cambia "us-east-1" por tu región

BUCKET_NAME = "vl-learning-audio-bucket"

@app.get("/")
def read_root():
    return {"message": "Hello World from VL Learning Backend using automated deployment"}

@app.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    try:
        # Lee el contenido del archivo
        file_content = await file.read()

        # Nombre único para el archivo (opcional)
        file_key = f"audios/{file.filename}"

        # Sube el archivo a S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_key,
            Body=file_content,
            ContentType=file.content_type
        )

        return {"message": "Archivo subido correctamente", "file_key": file_key}

    except Exception as e:
        print(f"Error al subir el archivo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al subir el archivo: {str(e)}")