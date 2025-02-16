from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from api.api_v1.endpoints import chatbot, upload, chat
from utils.interface import https_url_for

templates = Jinja2Templates(directory="templates")
templates.env.globals["https_url_for"] = https_url_for

api_router = APIRouter()

api_router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])