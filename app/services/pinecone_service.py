from pinecone import Pinecone, ServerlessSpec
import logging
from typing import List, Dict, Any
from datetime import datetime
from config.main import config
import json

logger = logging.getLogger(__name__)

class PineconeService:
    def __init__(self):
        self.pc = Pinecone(api_key=config.PINECONE_API_KEY)
        self.index_name = "knowledgebase"
        self._init_index()
        self.index = self.pc.Index(self.index_name)
        logger.info(f"Initialized PineconeService with index: {self.index_name}")

    def _init_index(self):
        """Initialize Pinecone index if it doesn't exist"""
        try:
            if self.index_name not in self.pc.list_indexes().names():
                self.pc.create_index(
                    name=self.index_name,
                    dimension=1536,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-east-1'
                    )
                )
                logger.info(f"Created new Pinecone index: {self.index_name}")
        except Exception as e:
            logger.error(f"Error initializing Pinecone index: {str(e)}")
            raise

    def _sanitize_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize metadata to ensure it's compatible with Pinecone
        """
        sanitized = {}
        for key, value in metadata.items():
            if isinstance(value, (str, int, float, bool)):
                sanitized[key] = value
            elif isinstance(value, list) and all(isinstance(x, str) for x in value):
                sanitized[key] = value
            elif isinstance(value, dict):
                # Convert nested dictionaries to strings
                sanitized[key] = str(value)
            else:
                # Convert other types to strings
                sanitized[key] = str(value)
        return sanitized

    async def store_embeddings(self, embeddings: List[List[float]], chunks: List[str], 
                             pdf_name: str, metadata: Dict):
        """Store embeddings with metadata in Pinecone"""
        try:
            vectors = []
            for i, (embedding, chunk) in enumerate(zip(embeddings, chunks)):
                # Create base metadata
                vector_metadata = {
                    "pdf_name": pdf_name,
                    "chunk_index": i,
                    "text": chunk,
                    "timestamp": datetime.utcnow().isoformat(),
                    "total_chars": metadata.get("total_chars", 0),
                    "total_words": metadata.get("total_words", 0),
                    "total_paragraphs": metadata.get("total_paragraphs", 0)
                }
                
                # Sanitize metadata
                vector_metadata = self._sanitize_metadata(vector_metadata)
                
                vector_id = f"{pdf_name}_chunk_{i}"
                vectors.append((vector_id, embedding, vector_metadata))

            self.index.upsert(vectors=vectors)
            logger.info(f"Stored {len(vectors)} embeddings for PDF: {pdf_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing embeddings: {str(e)}")
            raise 