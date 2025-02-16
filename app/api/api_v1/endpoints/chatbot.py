"""
This file contains the chatbot related endpoints
"""
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse

from utils.interface import https_url_for

router = APIRouter()

templates = Jinja2Templates(directory="templates")
templates.env.globals["https_url_for"] = https_url_for

@router.get("/", response_class=HTMLResponse)
async def call_chatbot(request: Request):
    """
    This function renders UI for the chatbot
    """
    return templates.TemplateResponse("chatbot.html", {"request": request})