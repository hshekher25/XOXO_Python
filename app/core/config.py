from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "XOXO Dating App"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "rootpassword"
    DB_NAME: str = "xoxo_db"
    
    # JWT
    JWT_SECRET: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Redis (optional - leave empty to disable)
    REDIS_URL: Optional[str] = None
    
    # S3/MinIO (optional - leave empty to disable photo uploads)
    S3_ENDPOINT_URL: Optional[str] = None
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET_NAME: str = "xoxo-images"
    S3_REGION: str = "us-east-1"
    
    # Location
    NEARBY_RADIUS_KM: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

