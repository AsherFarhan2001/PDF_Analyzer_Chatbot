"""
This file contains all the config read from .env file
"""
import os

class Base(object):
    """
    Base Configuration class. Contains the default configurations
    """

    DEBUG: bool = True
    TESTING: bool = False

class Config(Base):
    """
    Main Configuration class. Contains all the configurations for the project
    """

    OPENAI_API_KEY: str = (
        os.getenv("OPENAI_API_KEY") 
        or "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"
    )
    LLM_MODEL: str = os.getenv("LLM_MODEL") or "openai_gpt"
    PINECONE_API_KEY: str = (
        os.getenv("PINECONE_API_KEY") or "bceca74c-b1b7-4f81-b16a-ea19aabc053d"
    )

config = Config()
   