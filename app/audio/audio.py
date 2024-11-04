from fastapi import FastAPI, File, UploadFile, HTTPException
import boto3

app = FastAPI()

# El cliente de boto3 utilizará automáticamente el IAM Role asignado
s3 = boto3.client("s3", region_name="us-east-1")  # Cambia "us-east-1" por tu región

BUCKET_NAME = "nombre-de-tu-bucket"

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
        raise HTTPException(status_code=500, detail=f"Error al subir el archivo: {str(e)}")
