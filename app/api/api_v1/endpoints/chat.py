from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging
from services.embedding_service import EmbeddingService
from services.pinecone_service import PineconeService
from openai import OpenAI
from config.main import config
from constants.prompts import GENERAL_PROMPT, CONTEXT_PROMPT

logger = logging.getLogger(__name__)

router = APIRouter()
embedding_service = EmbeddingService()
pinecone_service = PineconeService()
openai_client = OpenAI(api_key=config.OPENAI_API_KEY)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    max_tokens: int = 1000
    temperature: float = 0.7

class ChatResponse(BaseModel):
    response: str

@router.post("/chat-completions")
async def chat_with_pdfs(request: ChatRequest) -> ChatResponse:
    """
    Chat endpoint that uses PDF knowledge base for context-aware responses
    """
    try:
        # Get the user's latest message
        user_query = request.messages[-1].content
        logger.info(f"Processing chat query: {user_query}")

        try:
            # Search relevant chunks from PDFs
            query_embedding = await embedding_service.create_embedding(user_query)
            logger.info("Created query embedding")
            search_results = pinecone_service.index.query(
                vector=query_embedding,
                top_k=4,
                include_metadata=True,
            )
            logger.info(f"Found {len(search_results.matches)} relevant chunks")
            print(search_results.matches)
            # Format context from relevant chunks
            context_chunks = []
            sources = []
            for match in search_results.matches:
                normalized_score = (1 + match.score) / 2
                logger.info(f"Raw score: {match.score}")
                # Convert score from [-1,1] to [0,1] range
                normalized_score = (1 + match.score) / 2
                logger.info(f"Normalized score: {normalized_score}")
                if normalized_score >= 0.5:
                    context_chunks.append(match.metadata.get("text", ""))
                    sources.append({
                        "pdf_name": match.metadata.get("pdf_name", ""),
                        "chunk_index": match.metadata.get("chunk_index", 0),
                        "relevance_score": match.score
                    })

            messages = []
            
            if context_chunks:
                # If relevant chunks found, use them as context
                context_text = "\n\n".join(context_chunks)
                system_prompt = CONTEXT_PROMPT.format(context=context_text)
                messages.append({"role": "system", "content": system_prompt})
                logger.info("Using PDF context for response")
                used_context = True
            else:
                # If no relevant chunks found, use a general conversation prompt
                messages.append({
                    "role": "system",
                    "content": GENERAL_PROMPT
                })
                logger.info("No relevant context found, using general conversation mode")
                used_context = False

            # Add conversation history (last 5 messages)
            history_messages = request.messages[-5:]
            for msg in history_messages:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

            logger.info("Sending request to OpenAI")
            response = openai_client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=messages,
                max_tokens=request.max_tokens,
                temperature=request.temperature
            )

            return ChatResponse(
                response=response.choices[0].message.content
            )

        except Exception as e:
            logger.error(f"Error during chat processing: {str(e)}")
            return ChatResponse(
                response="I encountered an error while processing your request. Please try again or rephrase your question.",
                sources=[]
            )

    except Exception as e:
        logger.error(f"Critical error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )
