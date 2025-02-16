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
    )
    LLM_MODEL: str = os.getenv("LLM_MODEL") or "openai_gpt"
    PINECONE_API_KEY: str = (
        os.getenv("PINECONE_API_KEY") or "pcsk_5ftniJ_F64PBDZE4rGxoqCPjP3sJ5aLkoB2WHW35WqkeY2DEUyq5pf1wik6SsibX55UvyC"
    )

config = Config()
   