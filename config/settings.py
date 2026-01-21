from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application Settings"""
   
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG_MODE: bool = True

     
    HF_TOKEN: str = ""
    OCR_MODEL: str = "microsoft/trocr-base-printed"

    MAX_FILE_SIZE: int = 10485760
    MAX_BATCH_SIZE: int = 10
    ALLOWED_EXTENSIONS: List[str]= ["pdf","docx","doc","txt","png","jpg","jpeg","tiff","bmp"]

    LOG_LEVEL: str = "INFO"

    TESSERACT_CMD: str = "/usr/bin/tesseract"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()