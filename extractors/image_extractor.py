"""
Image Extractor
Extract text from images using EasyOCR
"""

from PIL import Image
import io
import logging
import numpy as np

logger = logging.getLogger(__name__)


class ImageExtractor:
    """Extract text from images using EasyOCR"""
    
    def __init__(self, model_service):
        self.model_service = model_service
        self._easyocr_reader = None
    
    def _get_easyocr_reader(self):
        """Initialize EasyOCR reader lazily"""
        if self._easyocr_reader is None:
            try:
                import easyocr
                logger.info("Initializing EasyOCR (this takes a moment on first run)...")
                # English only - add more languages if needed: ['en', 'bn']
                self._easyocr_reader = easyocr.Reader(['en'], gpu=False)
                logger.info("EasyOCR ready!")
            except ImportError:
                raise Exception("EasyOCR not installed. Run: pip install easyocr")
        return self._easyocr_reader
    
    def extract(self, file_bytes: bytes, use_tesseract: bool = False) -> str:
        """
        Extract text from image using EasyOCR
        
        Args:
            file_bytes: Image file as bytes
            use_tesseract: Ignored (always uses EasyOCR)
        
        Returns:
            Extracted text
        """
        try:
            # Open image
            image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
            
            # Get EasyOCR reader
            reader = self._get_easyocr_reader()
            
            # Convert PIL Image to numpy array
            img_array = np.array(image)
            
            # Extract text
            logger.info("Extracting text using EasyOCR...")
            results = reader.readtext(img_array)
            
            # Combine all detected text
            text_lines = [result[1] for result in results]
            text = '\n'.join(text_lines)
            
            if not text.strip():
                return "No text found in image"
            
            logger.info(f"Successfully extracted {len(text)} characters")
            return text.strip()
            
        except Exception as e:
            logger.error(f"Image extraction failed: {str(e)}")
            raise Exception(f"Image extraction failed: {str(e)}")