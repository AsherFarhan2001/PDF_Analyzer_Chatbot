from openai import OpenAI
import logging
from config.main import config
from typing import List
from datetime import datetime
import numpy as np

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = "text-embedding-3-small"
        logger.info("Initialized EmbeddingService")

    def _normalize_vector(self, vector: List[float]) -> List[float]:
        """Normalize vector to unit length"""
        array = np.array(vector)
        norm = np.linalg.norm(array)
        if norm == 0:
            return vector
        return (array / norm).tolist()

    async def create_embedding(self, text: str) -> List[float]:
        """Create normalized embedding for a single text"""
        try:
            logger.info(f"Creating embedding for text length: {len(text)}")
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            embedding = response.data[0].embedding
            normalized_embedding = self._normalize_vector(embedding)
            logger.info("Successfully created normalized embedding")
            return normalized_embedding
        except Exception as e:
            logger.error(f"Error creating embedding: {str(e)}")
            raise

    async def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create normalized embeddings for multiple texts"""
        try:
            logger.info(f"Creating embeddings for {len(texts)} chunks")
            response = self.client.embeddings.create(
                model=self.model,
                input=texts
            )
            embeddings = [data.embedding for data in response.data]
            normalized_embeddings = [self._normalize_vector(emb) for emb in embeddings]
            logger.info(f"Successfully created {len(normalized_embeddings)} normalized embeddings")
            return normalized_embeddings
        except Exception as e:
            logger.error(f"Error creating embeddings: {str(e)}")
            raise

    async def store_embeddings(self, index, chunks: List[str], pdf_name: str, namespace: str = "knowledgebase"):
        """
        Store embeddings in Pinecone
        """
        try:
            # Generate embeddings for all chunks
            embeddings = await self.create_embeddings(chunks)
            
            # Prepare vectors with metadata
            vectors = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                metadata = {
                    "pdf_name": pdf_name,
                    "text": chunk,
                    "chunk_index": i,
                    "timestamp": str(datetime.utcnow())
                }
                vector_id = f"{pdf_name}_chunk_{i}"
                vectors.append((vector_id, embedding, metadata))
            
            # Upsert to Pinecone
            index.upsert(vectors=vectors, namespace=namespace)
            logger.info(f"Stored {len(vectors)} embeddings for PDF: {pdf_name}")
            
        except Exception as e:
            logger.error(f"Error storing embeddings: {str(e)}")
            raise 