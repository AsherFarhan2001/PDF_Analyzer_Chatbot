"""
The entry point for the FastAPI application
"""
import os
import certifi

# Add at the top of your main.py
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.router import api_router

app = FastAPI(title="PDF Analyzer Chatbot", version="1.0", debug=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router)