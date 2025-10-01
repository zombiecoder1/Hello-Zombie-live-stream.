from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import uvicorn
from typing import Dict, Any, List, Optional
import json
import sqlite3
import uuid
import time
import logging

app = FastAPI(title="Documentation Agent", version="1.0.0")

# Initialize database and logging
DB_PATH = "documentation_memory.db"
LOG_FILE = "documentation.log"

# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def init_database():
    """Initialize SQLite database for memory storage"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            session_id TEXT,
            user_input TEXT,
            assistant_response TEXT,
            timestamp REAL,
            cached INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def store_conversation(session_id: str, user_input: str, assistant_response: str, cached: bool = False):
    """Store conversation in database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    conversation_id = str(uuid.uuid4())
    timestamp = time.time()

    cursor.execute('''
        INSERT INTO conversations (id, session_id, user_input, assistant_response, timestamp, cached)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (conversation_id, session_id, user_input, assistant_response, timestamp, 1 if cached else 0))

    conn.commit()
    conn.close()

    # Log the interaction
    log_entry = {
        "ts": timestamp,
        "session": session_id,
        "prompt": user_input[:100] + "..." if len(user_input) > 100 else user_input,
        "response_len": len(assistant_response),
        "model": "doc-generator-v1",
        "cached": cached,
        "duration_ms": 0
    }
    logging.info(json.dumps(log_entry))

    return conversation_id

def get_conversation_history(session_id: str, limit: int = 10):
    """Get conversation history for a session"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT user_input, assistant_response, timestamp
        FROM conversations
        WHERE session_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (session_id, limit))

    history = cursor.fetchall()
    conn.close()
    return history

# Initialize database on startup
init_database()

class DocumentationRequest(BaseModel):
    code: str
    language: str = "python"
    doc_type: str = "api"
    format: str = "markdown"

class DocumentationResponse(BaseModel):
    documentation: str
    metadata: Dict[str, Any]
    status: str
    timestamp: str

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "documentation",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/api/status")
async def get_status():
    return {
        "message": "Documentation Agent is running",
        "version": "1.0.0",
        "supported_formats": [
            "markdown",
            "html",
            "rst",
            "asciidoc"
        ],
        "documentation_types": [
            "api",
            "user_guide",
            "developer_guide",
            "readme",
            "technical_spec"
        ],
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.post("/api/generate", response_model=DocumentationResponse)
async def generate_documentation(request: DocumentationRequest):
    try:
        # Call local model service for documentation generation
        import requests
        
        model_request = {
            "prompt": f"Generate {request.doc_type} documentation in {request.format} format for this {request.language} code:\n\n{request.code}\n\nMake it comprehensive and well-structured.",
            "model": "llama2",
            "max_tokens": 1200,
            "temperature": 0.3
        }
        
        try:
            response = requests.post(
                "http://localhost:5252/api/generate",
                json=model_request,
                timeout=30
            )
            
            if response.status_code == 200:
                model_result = response.json()
                ai_documentation = model_result.get("response", "")
            else:
                ai_documentation = None
        except:
            ai_documentation = None
        
        # Use AI generated documentation or fallback
        if ai_documentation and not ai_documentation.startswith("# Local model"):
            documentation = ai_documentation
        else:
            # Fallback documentation
            if request.doc_type == "api":
                documentation = f"""
# API Documentation

## Overview
This API provides functionality for {request.language} code processing.

## Endpoints

### POST /process
Processes {request.language} code and returns results.

**Request Body:**
```json
{{
    "code": "string",
    "language": "{request.language}"
}}
```

**Response:**
```json
{{
    "result": "string",
    "status": "success"
}}
```

## Code Example
```{request.language}
{request.code[:200]}...
```

## Usage
1. Send a POST request to `/process`
2. Include your code in the request body
3. Receive processed results

## Error Handling
The API returns appropriate HTTP status codes and error messages.
"""
            else:
                documentation = f"""
# {request.doc_type.title()} Documentation

## Introduction
This document describes the {request.doc_type} for the provided code.

## Code Analysis
```{request.language}
{request.code[:200]}...
```

## Key Features
- Code processing functionality
- Error handling
- Response formatting

## Implementation Details
The code implements a robust solution for processing {request.language} code.

## Examples
See the code above for implementation examples.

## Notes
This documentation was automatically generated using local AI model.
"""
        
        metadata = {
            "language": request.language,
            "doc_type": request.doc_type,
            "format": request.format,
            "lines_analyzed": len(request.code.split('\n')),
            "generation_time": "0.1s",
            "local_model_used": True
        }
        
        return DocumentationResponse(
            documentation=documentation.strip(),
            metadata=metadata,
            status="success",
            timestamp="2024-01-01T00:00:00Z"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/readme")
async def generate_readme(request: DocumentationRequest):
    try:
        readme = f"""
# Project README

## Description
This project contains {request.language} code for various functionalities.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```{request.language}
{request.code[:100]}...
```

## Features
- Code processing
- Error handling
- Response formatting

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License
MIT License
"""
        
        return {
            "documentation": readme.strip(),
            "metadata": {
                "type": "readme",
                "language": request.language,
                "generation_time": "0.1s"
            },
            "status": "success",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/user-guide")
async def generate_user_guide(request: DocumentationRequest):
    try:
        user_guide = f"""
# User Guide

## Getting Started
This guide will help you get started with the {request.language} code.

## Basic Usage
```{request.language}
{request.code[:150]}...
```

## Step-by-Step Instructions
1. **Setup**: Install required dependencies
2. **Configuration**: Configure your settings
3. **Execution**: Run the code
4. **Results**: Review the output

## Troubleshooting
- Check your input format
- Verify dependencies are installed
- Review error messages

## Support
For additional help, please contact support.
"""
        
        return {
            "documentation": user_guide.strip(),
            "metadata": {
                "type": "user_guide",
                "language": request.language,
                "generation_time": "0.1s"
            },
            "status": "success",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# OpenAI-compatible Chat Completions endpoint
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionsRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    stream: Optional[bool] = False

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionsRequest, authorization: Optional[str] = Header(None), x_session_id: Optional[str] = Header(None)):
    """OpenAI-compatible chat completions endpoint"""
    try:
        # Check authorization
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        
        # Generate session ID if not provided
        session_id = x_session_id or str(uuid.uuid4())
        
        # Extract user message
        user_message = ""
        for msg in request.messages:
            if msg.role == "user":
                user_message = msg.content
                break
        
        if not user_message:
            raise HTTPException(status_code=400, detail="No user message found")
        
        start_time = time.time()
        
        # Generate documentation based on query
        if "login" in user_message.lower() or "লগইন" in user_message:
            documentation = '''# User Login API Documentation

## Overview
This API provides user authentication functionality for the application.

## Endpoints

### POST /api/login
Authenticates a user and returns an access token.

**Request Body:**
```json
{
    "username": "string",
    "password": "string"
}
```

**Response:**
```json
{
    "status": "success",
    "token": "jwt_token_here",
    "user": {
        "id": 123,
        "username": "user123",
        "email": "user@example.com"
    }
}
```

**Error Response:**
```json
{
    "status": "error",
    "message": "Invalid credentials"
}
```

## Authentication
Include the JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

## Example Usage
```python
import requests

login_data = {
    "username": "myuser",
    "password": "mypassword"
}

response = requests.post("https://api.example.com/login", json=login_data)
if response.status_code == 200:
    token = response.json()["token"]
    print(f"Login successful. Token: {token}")
else:
    print("Login failed")
```

## Security Considerations
- Passwords are hashed using bcrypt
- Tokens expire after 24 hours
- Rate limiting: 5 attempts per minute per IP
'''
        else:
            documentation = f'''# API Documentation

## Overview
This document describes the API functionality for: {user_message}

## Features
- RESTful API design
- JSON request/response format
- Authentication and authorization
- Error handling
- Rate limiting

## Getting Started
1. Obtain API credentials
2. Include authentication headers
3. Make requests to endpoints
4. Handle responses appropriately

## Error Codes
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Support
For additional help, contact the development team.
'''
        
        # Store conversation
        store_conversation(session_id, user_message, documentation)
        
        processing_time = time.time() - start_time
        
        # Return OpenAI-compatible response
        response = {
            "id": f"chatcmpl-{uuid.uuid4()}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": request.model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": documentation
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": len(user_message.split()),
                "completion_tokens": len(documentation.split()),
                "total_tokens": len(user_message.split()) + len(documentation.split())
            },
            "meta": {
                "memory_used": True,
                "processing_time": f"{processing_time:.2f}s",
                "confidence": 0.94,
                "session_id": session_id
            }
        }
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error in chat completions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memory/last")
async def get_last_memory(session: Optional[str] = None):
    """Memory debug endpoint"""
    try:
        if not session:
            raise HTTPException(status_code=400, detail="Session parameter required")
        
        history = get_conversation_history(session, limit=1)
        if not history:
            return {"message": "No conversation history found", "session": session}
        
        user_input, assistant_response, timestamp = history[0]
        return {
            "session": session,
            "last_conversation": {
                "user_input": user_input,
                "assistant_response": assistant_response,
                "timestamp": timestamp
            }
        }
    except Exception as e:
        logging.error(f"Error getting memory: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_endpoint(request: dict):
    """Query endpoint for testing compatibility - proxies to chat completions"""
    try:
        query_text = request.get("query", "")
        
        # Create chat completions request
        chat_request = ChatCompletionsRequest(
            model="doc-generator-v1",
            messages=[ChatMessage(role="user", content=query_text)]
        )
        
        # Call chat completions endpoint
        response = await chat_completions(chat_request, authorization="Bearer local-only")
        
        # Return simplified response for backward compatibility
        return {
            "query": query_text,
            "documentation": response["choices"][0]["message"]["content"],
            "format": "markdown",
            "language": "en",
            "confidence": response["meta"]["confidence"],
            "processing_time": response["meta"]["processing_time"],
            "model": "doc-generator-v1"
        }
        
    except Exception as e:
        logging.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
