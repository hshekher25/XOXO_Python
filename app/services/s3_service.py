import boto3
from botocore.config import Config
from fastapi import UploadFile
from app.core.config import settings
import uuid


class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            config=Config(signature_version="s3v4"),
            region_name=settings.S3_REGION,
        )
        self.bucket_name = settings.S3_BUCKET_NAME

    async def upload_file(self, file: UploadFile, prefix: str = "") -> str:
        file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
        file_key = f"{prefix}{uuid.uuid4()}.{file_extension}"
        
        contents = await file.read()
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=file_key,
            Body=contents,
            ContentType=file.content_type,
        )
        
        # Return public URL
        if settings.S3_ENDPOINT_URL:
            return f"{settings.S3_ENDPOINT_URL}/{self.bucket_name}/{file_key}"
        return f"https://{self.bucket_name}.s3.amazonaws.com/{file_key}"

