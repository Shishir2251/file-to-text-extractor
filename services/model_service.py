from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import logging
from config.settings import settings
logger = logging.getLogger (__name__)


class Modelservice:
    def __init__(self):
        self.ocr_processor = None
        self.ocr_model = None 
        self._models_loaded = False

    def load_model(self):
        try:
            logger.info(f"Loading OCR model: {settings.OCR_MODEL}")
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
        return self._models_loaded
    def get_ocr_processor(self):
        return self.ocr_processor
    def get_ocr_model(self):
        return self.ocr_model