from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import logging

from services.extraction_service import ExtractionService
from services.model_service import ModelService
from utils.file_detector import FileDetector
from config.settings import settings


logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="File to Text Extraction API",
    description="Extract text from images, PDFs, DOCX, and text files",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


model_service = ModelService()
extraction_service = ExtractionService(model_service)
file_detector = FileDetector()


@app.on_event("startup")
async def startup_event():
    """Load models on startup"""
    logger.info("Starting File to Text Extraction API...")
    model_service.load_models()
    logger.info("API ready!")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "File to Text Extraction API",
        "status": "running",
        "version": "1.0.0",
        "supported_formats": ["PDF", "DOCX", "TXT", "Images (PNG, JPG, TIFF, BMP)"]
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "models_loaded": model_service.is_loaded(),
        "settings": {
            "max_file_size": settings.MAX_FILE_SIZE,
            "allowed_extensions": settings.ALLOWED_EXTENSIONS
        }
    }


@app.post("/extract")
async def extract_text(
    file: UploadFile = File(...),
    use_tesseract: Optional[bool] = False
):
    """
    Extract text from uploaded file
    
    Parameters:
    - file: The file to extract text from
    - use_tesseract: Force use of Tesseract for OCR (optional)
    
    Returns:
    - JSON with extracted text and metadata
    """
    try:
       
        file_bytes = await file.read()
        
       
        if len(file_bytes) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE / 1024 / 1024}MB"
            )
        
        
        mime_type = file_detector.detect_mime_type(file_bytes, file.filename)
        
        logger.info(f"Processing file: {file.filename} (MIME: {mime_type})")
        
        
        result = extraction_service.extract_text(
            file_bytes=file_bytes,
            mime_type=mime_type,
            filename=file.filename,
            use_tesseract=use_tesseract
        )
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


@app.post("/extract-batch")
async def extract_text_batch(files: List[UploadFile] = File(...)):
    """
    Extract text from multiple files
    
    Parameters:
    - files: List of files to extract text from
    
    Returns:
    - JSON with extracted text from all files
    """
    if len(files) > settings.MAX_BATCH_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Too many files. Maximum batch size: {settings.MAX_BATCH_SIZE}"
        )
    
    results = []
    
    for file in files:
        try:
            file_bytes = await file.read()
            
            if len(file_bytes) > settings.MAX_FILE_SIZE:
                results.append({
                    "filename": file.filename,
                    "success": False,
                    "error": "File too large"
                })
                continue
            
            mime_type = file_detector.detect_mime_type(file_bytes, file.filename)
            
            result = extraction_service.extract_text(
                file_bytes=file_bytes,
                mime_type=mime_type,
                filename=file.filename
            )
            
            results.append({
                "filename": file.filename,
                "success": result["success"],
                "text": result.get("text"),
                "mime_type": result.get("mime_type"),
                "extraction_method": result.get("extraction_method")
            })
            
        except Exception as e:
            logger.error(f"Error processing {file.filename}: {str(e)}")
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })
    
    return JSONResponse(content={"results": results, "total": len(results)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        log_level=settings.LOG_LEVEL.lower()
    )