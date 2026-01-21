import logging
from typing import Dict
from extractors.image_extractor import ImageExtractor
from extractors.pdf_extractor import PDFExtractor
from extractors.docx_extractor import DOCXExtractor
from extractors.text_extractor import TEXTExtractor
from services.model_service import Modelservice

logger = logging.getLogger(__name__)

class ExtractionService:

    def __init__(self, model_service: Modelservice):
        self.model_service = model_service
        self.image_extractor = ImageExtractor(model_service)
        self.pdf_extractor = PDFExtractor()
        self.docx_extractor = DOCXExtractor()
        self.text_extractor = DOCXExtractor()

    def extract_text(
            self,
            file_bytes: bytes,
            mime_type: str,
            filename: str,
            use_tesseract: bool=False
    ) -> Dict:
        """
        Extract text from file based on MIME type
        
        Args:
            file_bytes: File content as bytes
            mime_type: MIME type of the file
            filename: Name of the file
            use_tesseract: Force use of Tesseract for OCR
        
        Returns:
            Dictionary with extraction results
        """
        try:
            if mime_type == 'application/pdf':
                text = self.pdf_extractor.extract(file_bytes)
                method = "PDF extraction"
            elif mime_type in [
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/msword'
            ]:
                text = self.docx_extractor.extract(file_bytes)
                method = "DOCX extraction"
            elif mime_type.startswith('text/'):
                text = self.text_extractor.extract(file_bytes)
                method = "Text file reading"
            elif mime_type.startswith('image/'):
                text = self.image_extractor.extract(file_bytes,use_tesseract)
                method = "Tesseract OCR" if use_tesseract or not self.model_service.is_loaded() else "TrOCR"
            else:
                raise ValueError(f"Unsuported file type: {mime_type}")
            return {
                "success": True,
                "filename": filename,
                "mime_type": mime_type,
                "extraction_method": method,
                "text": text,
                "character_count": len(text),
                "word_count": len (text.split())
                     }
        except Exception as e:
            logger.errror(f"\Extraction failed for {filename}: {str(e)}")
            raise

            
                

        
