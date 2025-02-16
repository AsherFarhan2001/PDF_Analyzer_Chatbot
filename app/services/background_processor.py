from services.embedding_service import EmbeddingService
from services.pinecone_service import PineconeService
import logging
from typing import List, Dict
import asyncio

logger = logging.getLogger(__name__)

class BackgroundProcessor:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.pinecone_service = PineconeService()
        logger.info("Initialized BackgroundProcessor")

    async def process_chunks(self, chunks: List[str], pdf_name: str, metadata: Dict):
        """Process chunks in background"""
        try:
            logger.info(f"Starting background processing for {pdf_name}")
            
            # Extract only the necessary metadata
            simplified_metadata = {
                "total_chars": metadata.get("total_chars", 0),
                "total_words": metadata.get("total_words", 0),
                "total_paragraphs": metadata.get("total_paragraphs", 0)
            }
            
            # Create embeddings
            embeddings = await self.embedding_service.create_embeddings(chunks)
            
            # Store in Pinecone with simplified metadata
            await self.pinecone_service.store_embeddings(
                embeddings=embeddings,
                chunks=chunks,
                pdf_name=pdf_name,
                metadata=simplified_metadata
            )
            
            logger.info(f"Completed background processing for {pdf_name}")
            return True
        except Exception as e:
            logger.error(f"Error in background processing: {str(e)}")
            raise 