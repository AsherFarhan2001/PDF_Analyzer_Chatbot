from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from typing import List
from pathlib import Path
from services.pdf_extracter import PDFExtractorService
from services.text_processor import TextProcessorService
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
pdf_service = PDFExtractorService()
text_processor = TextProcessorService()

# Configure upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Endpoint to handle PDF file uploads and text extraction
    """
    try:
        processed_files = []
        
        for file in files:
            if not file.filename.lower().endswith('.pdf'):
                raise HTTPException(
                    status_code=400,
                    detail=f"File {file.filename} is not a PDF"
                )
            
            # Create safe filename
            file_path = UPLOAD_DIR / file.filename
            print(file_path)
            
            # Save file
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            # Process PDF and extract text, and create chunks
            result = await pdf_service.process_pdf(file_path)
            processed_files.append(result)
        
        return {
            "message": "Files processed successfully",
            "processed_files": processed_files
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing files: {str(e)}"
        )

@router.get("/text/{filename}")
async def get_processed_text(filename: str, include_chunks: bool = False):
    """
    Get processed text from a PDF file with chunks
    """
    try:
        logger.info(f"Text retrieval called for file: {filename}")
        result = await pdf_service.get_text_by_filename(filename)
        
        if result["status"] == "error":
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Unknown error occurred")
            )
        
        response = {
            "filename": filename,
            "text": result["text"],
            "stats": result["stats"],
            "status": "success"
        }
        
        if include_chunks:
            response["chunks"] = result["chunks"]
        
        return response
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {filename}")
        raise HTTPException(
            status_code=404,
            detail=f"File {filename} not found"
        )
    except Exception as e:
        logger.error(f"Error getting text: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting text: {str(e)}"
        )