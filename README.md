# File to Text Extraction API

A modular, well-structured FastAPI application for extracting text from various file formats using free Hugging Face models.

## 🏗️ Project Structure

```
file-to-text-extractor/
│
├── main.py                          # FastAPI application entry point
│
├── config/
│   ├── __init__.py
│   └── settings.py                  # Configuration and environment variables
│
├── services/
│   ├── __init__.py
│   ├── model_service.py             # ML model loading and management
│   └── extraction_service.py        # Orchestrates extraction logic
│
├── extractors/
│   ├── __init__.py
│   ├── image_extractor.py           # OCR for images
│   ├── pdf_extractor.py             # PDF text extraction
│   ├── docx_extractor.py            # Word document extraction
│   └── text_extractor.py            # Plain text file extraction
│
├── utils/
│   ├── __init__.py
│   └── file_detector.py             # File type detection
│
├── .env                             # Environment configuration
├── .gitignore                       # Git ignore rules
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## ✨ Features

- **Modular Architecture**: Clean separation of concerns
- **Multiple File Formats**: Images, PDFs, DOCX, TXT
- **Free ML Models**: Uses Microsoft's TrOCR from Hugging Face
- **Fallback Support**: Tesseract OCR as backup
- **Batch Processing**: Handle multiple files at once
- **Type Safety**: Pydantic models for validation
- **Logging**: Comprehensive logging throughout

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd file-to-text-extractor
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Tesseract OCR (Optional but recommended)

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download and install from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

### 5. Configure environment

```bash
cp .env.example .env
# Edit .env with your settings
```

## 🎯 Usage

### Start the server

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### API Endpoints

#### Health Check
```bash
GET /
GET /health
```

#### Extract Text from Single File
```bash
POST /extract
```

Example:
```bash
curl -X POST "http://localhost:8000/extract" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

#### Extract Text from Multiple Files
```bash
POST /extract-batch
```

Example:
```bash
curl -X POST "http://localhost:8000/extract-batch" \
  -F "files=@doc1.pdf" \
  -F "files=@image.png" \
  -F "files=@doc2.docx"
```

### Python Client Example

```python
import requests

# Single file
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/extract', files=files)
    result = response.json()
    print(result['text'])

# Batch processing
files = [
    ('files', open('doc1.pdf', 'rb')),
    ('files', open('image1.png', 'rb')),
]
response = requests.post('http://localhost:8000/extract-batch', files=files)
print(response.json())
```

## 📦 Components Explained

### `main.py`
- FastAPI application setup
- Route definitions
- Request handling
- CORS configuration

### `config/settings.py`
- Environment variable management
- Configuration using Pydantic
- Centralized settings

### `services/model_service.py`
- Loads and manages ML models
- TrOCR model initialization
- Model state management

### `services/extraction_service.py`
- Orchestrates text extraction
- Routes requests to appropriate extractors
- Aggregates results

### `extractors/`
- **image_extractor.py**: OCR using TrOCR or Tesseract
- **pdf_extractor.py**: PDF text extraction using PyPDF2
- **docx_extractor.py**: Word document extraction
- **text_extractor.py**: Plain text file reading

### `utils/file_detector.py`
- MIME type detection
- File type identification
- Extension-based fallback

## 🔧 Configuration

Edit `.env` file:

```env
# API
API_HOST=0.0.0.0
API_PORT=8000

# Models
OCR_MODEL=microsoft/trocr-base-printed
HF_TOKEN=  # Optional: Your Hugging Face token

# Files
MAX_FILE_SIZE=10485760  # 10MB
MAX_BATCH_SIZE=10

# Logging
LOG_LEVEL=INFO
```

## 🧪 Testing

```python
# Test with Python
import requests

response = requests.post(
    'http://localhost:8000/extract',
    files={'file': open('test.pdf', 'rb')}
)
print(response.json())
```

## 📊 Supported Formats

| Format | Extension | Extractor |
|--------|-----------|-----------|
| PDF | .pdf | PyPDF2 |
| Word | .docx, .doc | python-docx |
| Text | .txt | Built-in |
| Images | .png, .jpg, .jpeg, .tiff, .bmp | TrOCR/Tesseract |

## 🤖 Models Used

- **TrOCR**: `microsoft/trocr-base-printed` (~500MB)
- **License**: MIT
- **Source**: [Hugging Face](https://huggingface.co/microsoft/trocr-base-printed)

## 🐛 Troubleshooting

### Model download fails
- Check internet connection
- Ensure sufficient disk space (~1GB)
- Set `HF_TOKEN` in `.env`

### Import errors
```bash
# Make sure all __init__.py files exist
touch config/__init__.py
touch services/__init__.py
touch extractors/__init__.py
touch utils/__init__.py
```

### Tesseract not found
```bash
sudo apt-get install tesseract-ocr

# Set path in .env
TESSERACT_CMD=/usr/bin/tesseract
```

## 📝 License

MIT License

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.