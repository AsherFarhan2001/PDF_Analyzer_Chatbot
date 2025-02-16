from pathlib import Path
import fitz  # PyMuPDF
from typing import Dict, Optional
import logging
import re
from services.text_processor import TextProcessorService
from services.background_processor import BackgroundProcessor
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFExtractorService:
    """Service class for handling PDF text extraction"""
    
    def __init__(self):
        self.upload_dir = Path("uploads")
        self.upload_dir.mkdir(exist_ok=True)
        self.text_processor = TextProcessorService()
        self.background_processor = BackgroundProcessor()
        logger.info(f"PDFExtractorService initialized with upload dir: {self.upload_dir}")

    async def extract_text_from_pdf(self, file_path: Path) -> str:
        """
        Extract text content from a PDF file with improved extraction
        """
        try:
            logger.info(f"Attempting to extract text from: {file_path}")
            doc = fitz.open(file_path)
            text = ""
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Get text with more detailed parameters
                text += page.get_text(
                    sort=True, 
                    flags=fitz.TEXT_PRESERVE_LIGATURES | 
                          fitz.TEXT_PRESERVE_WHITESPACE |
                          fitz.TEXT_PRESERVE_SPANS |
                          fitz.TEXT_DEHYPHENATE 
                )
                text += "\n\n"
                
                if page_num % 10 == 0:
                    logger.info(f"Processed {page_num + 1} pages of {len(doc)}")
            
            doc.close()
            logger.info(f"Successfully extracted text from: {file_path}")
            
            # Clean the extracted text
            text = self.clean_text(text)
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    def clean_text(self, text: str) -> str:
        """
        Clean the extracted text by removing special characters, URLs, and normalizing whitespace
        """
        try:
            # Remove URLs
            text = re.sub(r'http[s]?://\S+', '', text)
            text = re.sub(r'www\.\S+', '', text)
            
            # Remove email addresses
            text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '', text)
            
            # Replace special characters and symbols
            text = re.sub(r'[^\w\s.,!?;:\'\"\(\)\[\]\{\}\-]', ' ', text)
            
            # Normalize whitespace
            text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
            text = re.sub(r'\n\s*\n', '\n\n', text)  # Normalize paragraph breaks
            
            # Remove leading/trailing whitespace from each line
            text = '\n'.join(line.strip() for line in text.split('\n'))
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error cleaning text: {str(e)}")
            return text

    async def process_pdf(self, file_path: Path) -> Dict[str, Optional[str]]:
        """
        Process a PDF file and extract its text content
        """
        try:
            logger.info(f"Processing PDF file: {file_path}")
            
            # Extract and clean text
            extracted_text = await self.extract_text_from_pdf(file_path)
            
            # Create chunks
            chunk_result = await self.text_processor.process_and_chunk_text(extracted_text)
            
            # Create simplified stats
            stats = {
                "total_chars": len(extracted_text),
                "total_words": len(extracted_text.split()),
                "total_paragraphs": len(extracted_text.split('\n\n'))
            }

            # Start background processing
            asyncio.create_task(
                self.background_processor.process_chunks(
                    chunks=chunk_result["chunks"],
                    pdf_name=file_path.name,
                    metadata=stats
                )
            )
            
            return {
                "filename": file_path.name,
                "status": "success",
                "message": "PDF processed, embeddings being generated in background"
            }
            
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            return {
                "filename": file_path.name,
                "status": "error",
                "error": str(e)
            }

    async def get_text_by_filename(self, filename: str) -> Dict[str, Optional[str]]:
        """
        Get text from a specific PDF file by filename
        """
        try:
            file_path = self.upload_dir / filename
            logger.info(f"Looking for file: {file_path}")
            
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                raise FileNotFoundError(f"File {filename} not found")
                
            return await self.process_pdf(file_path)
            
        except Exception as e:
            logger.error(f"Error in get_text_by_filename: {str(e)}")
            raise Exception(str(e))