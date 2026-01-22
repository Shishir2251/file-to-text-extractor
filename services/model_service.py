"""
Model Service
Handles loading and managing ML models
"""

from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import logging

logger = logging.getLogger(__name__)


class ModelService:
    """Service for managing ML models"""
    
    def __init__(self):
        self.ocr_processor = None
        self.ocr_model = None
        self._models_loaded = False
    
    def load_models(self):
        """Load TrOCR model from Hugging Face"""
        try:
            from config.settings import settings
            
            logger.info(f"Loading OCR model: {settings.OCR_MODEL}")
            
            # Load TrOCR processor and model
            self.ocr_processor = TrOCRProcessor.from_pretrained(
                settings.OCR_MODEL,
                token=settings.HF_TOKEN if settings.HF_TOKEN else None
            )
            
            self.ocr_model = VisionEncoderDecoderModel.from_pretrained(
                settings.OCR_MODEL,
                token=settings.HF_TOKEN if settings.HF_TOKEN else None
            )
            
            self._models_loaded = True
            logger.info("OCR model loaded successfully")
            
        except Exception as e:
            logger.warning(f"Failed to load TrOCR model: {e}")
            logger.info("Will use Tesseract OCR as fallback")
            self._models_loaded = False
    
    def is_loaded(self) -> bool:
        """Check if models are loaded"""
        return self._models_loaded
    
    def get_ocr_processor(self):
        """Get OCR processor"""
        return self.ocr_processor
    
    def get_ocr_model(self):
        """Get OCR model"""
        return self.ocr_model