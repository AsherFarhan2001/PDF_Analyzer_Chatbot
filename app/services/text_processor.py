from typing import List
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextProcessorService:
    """Service for processing and chunking text"""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Characters per chunk
            chunk_overlap=100,  # Overlap between chunks
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", " ", ""]  # Priority order for splitting
        )
    
    async def create_chunks(self, text: str) -> List[str]:
        """
        Split text into chunks using LangChain's text splitter
        Args:
            text (str): Preprocessed text to be chunked
        Returns:
            List[str]: List of text chunks
        """
        try:
            logger.info("Starting text chunking process")
            
            # Create chunks
            chunks = self.text_splitter.split_text(text)
            chunk_sizes = [len(chunk) for chunk in chunks]
            avg_size = sum(chunk_sizes) / len(chunks)
            size_variance = sum((size - avg_size) ** 2 for size in chunk_sizes) / len(chunks)
            
            # Log chunking results
            logger.info(f"Successfully created {len(chunks)} chunks")
            logger.info(f"Average chunk size: {sum(len(chunk) for chunk in chunks) / len(chunks):.2f} characters")
            
            return chunks
            
        except Exception as e:
            logger.error(f"Error during text chunking: {str(e)}")
            raise

    async def process_and_chunk_text(self, text: str) -> dict:
        """
        Process text and return chunks with metadata
        Args:
            text (str): Text to process and chunk
        Returns:
            dict: Dictionary containing chunks and metadata
        """
        try:
            # Create chunks
            chunks = await self.create_chunks(text)
            
            # Create metadata about chunks
            metadata = {
                "total_chunks": len(chunks),
                "chunk_sizes": [len(chunk) for chunk in chunks],
                "average_chunk_size": sum(len(chunk) for chunk in chunks) / len(chunks)
            }
            
            return {
                "chunks": chunks,
                "metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"Error in process_and_chunk_text: {str(e)}")
            raise 