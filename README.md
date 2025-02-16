# PDF_Analyzer_Chatbot
This repository will host PDF_Analyzer Code
=======

# PDF_Analyzer_Chatbot

The PDF Analyzer Chatbot is a FastAPI-based microservice designed to extract text from PDFs, preprocess it, and store it in a vector database (Pinecone) after converting it into embeddings. The chatbot leverages OpenAI's Language Model (LLM) and LangChain for text chunking and embedding generation. It allows users to query the stored PDF content using natural language and retrieve relevant information.

## Features

- **Natural Language Processing**: Understands and processes requests in natural language.
- **Task Automation**: Automates routine PDF analysis tasks, including text extraction and semantic searches.
- **FastAPI Framework**: Ensures high performance, easy scalability, and real-time request handling.
- **API Versioning**: Supports future expansions and iterations with minimal disruptions.
- **Vector Database** : Stores embeddings in Pinecone for efficient semantic search.
- **PDF Text Extraction**: Extracts text from uploaded PDF files.

## Functionalities

- **Upload PDF**: Allows users to upload PDFs and automatically extract text which then converts into chunks.
- **Store in Pinecone**: Saves embeddings in Pinecone for efficient future searches.
- **Contextual Query**: Responses: Uses relevant chunks as context to provide accurate and detailed responses.
- **Create Embeddings**: Converts text chunks into embeddings using OpenAI's embedding model.

## Project Structure

The project follows a modular and scalable structure, designed for maintainability and ease of development:

- `app/`: Core application code, including API endpoints and utilities.
    - `app/main.py`: Application entry point and FastAPI configuration.
    - `app/services/`: Business logic and service layer for handling requests.
    - `app/utils/`: Utility functions and helper modules.
    - `app/templates/`: HTML templates for the web interface.
    - `app/static/`: Static files for the web interface.
    - `app/config/`: Configuration settings and environment variables.
    - `app/constants/`: Constants and enumerations.
- `requirements.txt`: List of project dependencies.

## Getting Started

To set up the PDF Analyzer chatbot microservice, follow the steps below:

1. **Clone the Repository**:
```bash
git clone https://github.com/AsherFarhan2001/PDF_Analyzer_Chatbot.git
```

2. **Create Virtual Environment**:
```bash
conda create -n chatbot-test
```
3. **Activate Virtual Environment**:
```bash
python3 -m venv env
source activate chatbot-test
cd app
```

4. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

5. **Run the FastAPI Project**:
```bash
uvicorn main:app --reload
```
6. **Access the Project**:
```bash
http://localhost:8000/chatbot/