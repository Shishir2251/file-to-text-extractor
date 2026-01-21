import PyPDF2
import io
import logging

logger = logging.getLogger(__name__)


class PDFExractor:
    def extract(self,file_bytes: bytes) -> str:
        """
        Extract text from PDF
        
        Args:
            file_bytes: PDF file as bytes
        
        Returns:
            Extracted text
        """
        try:
            pdf_file = io.BytesIO(file_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text += page_text +"\n"
                    if not text.strip():
                        raise Exception("No text found in pdf,IT Might be scanned or image-based.")
            return text.strip()
        except Exception as e:
            logger.error(f"PDF extraction failed: {str(e)}")
            raise Exception(f"PDF extraction failed : {str(e)}")
