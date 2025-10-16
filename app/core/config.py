from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_DESCRIPTION: str
    VERSION: str
    API_V1_STR: str
    DATABASE_URL: str
    ALEMBIC_URL: str
    SECRET_KEY: str
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    BACKEND_CORS_ORIGINS: list

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"

settings = Settings()



