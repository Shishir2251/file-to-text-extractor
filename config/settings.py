"""
Configuration Settings
Load settings from environment variables
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG_MODE: bool = True
    
    # Hugging Face Configuration
    HF_TOKEN: str = ""
    OCR_MODEL: str = "microsoft/trocr-base-printed"
    
    # File Processing Configuration
    MAX_FILE_SIZE: int = 10485760  # 10MB in bytes
    MAX_BATCH_SIZE: int = 10
    ALLOWED_EXTENSIONS: str = "pdf,docx,doc,txt,png,jpg,jpeg,tiff,bmp"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Tesseract Configuration
    TESSERACT_CMD: str = "/usr/bin/tesseract"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()