import boto3
s3 = boto3.client('s3')

AWS_S3_BUCKET_NAME = "vl-learning-bucket"

def upload_image_to_s3(image_path: str, image_key: str) -> str:
    s3.upload_file(image_path, AWS_S3_BUCKET_NAME, image_key)

    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': AWS_S3_BUCKET_NAME, 'Key': image_key},
        ExpiresIn=3600  # 1 hora
    )

    return url