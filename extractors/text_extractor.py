"""
Text Extractor
Extract text from plain text files
"""

import logging

logger = logging.getLogger(__name__)


class TextExtractor:
    """Extract text from text files"""
    
    ENCODINGS = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'ascii']
    
    def extract(self, file_bytes: bytes) -> str:
        """
        Extract text from text file
        
        Args:
            file_bytes: Text file as bytes
        
        Returns:
            Extracted text
        """
        # Try different encodings
        for encoding in self.ENCODINGS:
            try:
                text = file_bytes.decode(encoding)
                return text.strip()
            except UnicodeDecodeError:
                continue
        
        # If all encodings fail
        raise Exception(
            f"Could not decode text file with any supported encoding: {', '.join(self.ENCODINGS)}"
        )