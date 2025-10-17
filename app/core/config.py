from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_DESCRIPTION: str
    VERSION: str
    API_V1_STR: str
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    BACKEND_CORS_ORIGINS: list

    # MinIO Configuration
    MINIO_ENDPOINT: str = "zoka-minio:9000"
    MINIO_EXTERNAL_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str 
    MINIO_SECRET_KEY: str 
    MINIO_BUCKET_NAME: str 
    MINIO_USE_SSL: bool = False

    # Email Configuration
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = "noreply@zokatoolbox.com"
    MAIL_FROM_NAME: str = "Zoka Platform"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = ""
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = False
    MAIL_USE_CREDENTIALS: bool = False
    MAIL_VALIDATE_CERTS: bool = False

    # Frontend URL for email links
    FRONTEND_URL: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"

settings = Settings()



