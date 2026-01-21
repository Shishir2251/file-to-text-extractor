import magic
import logging

logger= logging.getLogger(__name__)

class FileDetector:
    Mime_map= {
         'pdf': 'application/pdf',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'doc': 'application/msword',
        'txt': 'text/plain',
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'tiff': 'image/tiff',
        'tif': 'image/tiff',
        'bmp': 'image/bmp',
        'gif': 'image/gif'
    }

    def detect_mime_type(self, file_bytes: bytes, filename: str) -> str:
        """
        Detect MIME type of file
        
        Args:
            file_bytes: File content as bytes
            filename: Name of the file
        
        Returns:
            MIME type string
        """
        try:
            mime = magic.from_buffer(file_bytes, mime=True)
            logger.info(f"Detected MIME type using magic: {mime}")
            return mime
        except Exception as e:
            logger.warning(f"Magic Detection failed: {e}.Using extension fallback.")
            return self._detect_from_extension(filename)
    
    def _detect_from_extension(self, filename: str) -> str:
        """
        Detect MIME type from file extension
        
        Args:
            filename: Name of the file
        
        Returns:
            MIME type string
        """
        ext= filename.lower().split('.')[-1] if '.' in filename else''
        mime_type = self.MIME_MAP.get(ext, 'application/octet-stream')
        logger.info(f"Detected MIME type from extension: {mime_type}")
        return mime_type
