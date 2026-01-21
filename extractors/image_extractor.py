from PIL import Image
import pytesseract
import io
import logging

from sympy import false
from services.model_service import Modelservice
from config.settings import settings

logger = logging.getLogger(__name__)

class ImageExtractor:

    def __int__(self, model_service: Modelservice):
        self.model_service = model_service

        if settings.TESSERACT_CMD:
            pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
    def extract(self, file_bytes: bytes, use_tesseract: bool = false) -> str:
        """
        Extract text from image
        
        Args:
            file_bytes: Image file as bytes
            use_tesseract: Force use of Tesseract OCR
        
        Returns:
            Extracted text
        """
        try:
            image = Image.open(io.BytesIO(file_bytes)).convert("RGB")

            if use_tesseract or not self.model_service.is_loaded():
                return self._extract_with_tesseract(image)
            
            return self._extract_with_trocr(image)
        
        except Exception as e:
            logger.error(f"Image extractor failed: {str(e)}")
            raise
    def _extract_with_trocr(self, image: Image.Image) -> str:
        try:
            processor = self.model_service.get_ocr_processor()
            model = self.model_service.get_ocr_model()

            pixel_values = processor(image, return_tensors="pt").pixel_values

            generated_ids = model.generate(pixel_values)
            text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            return text.strip()
        except Exception as e:
            raise Exception(f"TrOCR failed: {str(e)}")
        