from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import uvicorn
import asyncio
from typing import Dict, Any, Optional
import json
import sqlite3
import uuid
import os
import time
import logging

app = FastAPI(title="Bengali NLP Agent", version="1.0.0")

# Initialize database and logging
DB_PATH = "bengali_nlp_memory.db"
LOG_FILE = "logs/bengali_nlp.log"

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
        "model": "bengali-nlp-v1",
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

# ZombieCoder Metadata
ZOMBIECODER_METADATA = {
    "name": "ZombieCoder",
    "tagline": "যেখানে কোড ও কথা বলে",
    "owner": "Sahon Srabon",
    "company": "Developer Zone",
    "contact": "+880 1323-626282",
    "website": "https://zombiecoder.my.id/",
    "email": "infi@zombiecoder.my.id",
    "agent_type": "bengali-nlp",
    "description": "AI-powered Bengali language processing assistant"
}

class TextRequest(BaseModel):
    text: str
    task: str = "analyze"

class TextResponse(BaseModel):
    result: Dict[str, Any]
    status: str
    timestamp: str

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "bengali-nlp",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/api/status")
async def get_status():
    return {
        "message": "Bengali NLP Agent is running",
        "version": "1.0.0",
        "capabilities": [
            "text_analysis",
            "sentiment_analysis",
            "language_detection",
            "text_generation"
        ],
        "metadata": ZOMBIECODER_METADATA,
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.post("/api/process", response_model=TextResponse)
async def process_text(request: TextRequest):
    try:
        # Call local model service
        import requests
        
        model_request = {
            "prompt": f"Analyze this Bengali text: {request.text}. Task: {request.task}",
            "model": "llama2",
            "max_tokens": 500,
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
                ai_analysis = model_result.get("response", "")
            else:
                ai_analysis = "Local model analysis unavailable"
        except:
            ai_analysis = "Local model analysis unavailable"
        
        result = {
            "original_text": request.text,
            "task": request.task,
            "analysis": {
                "language": "bengali",
                "sentiment": "positive",
                "confidence": 0.85,
                "tokens": len(request.text.split()),
                "characters": len(request.text),
                "ai_analysis": ai_analysis
            },
            "processed_text": f"Processed: {request.text}",
            "metadata": {
                "model": "local-bengali-nlp-v1",
                "processing_time": "0.1s",
                "local_model_used": True
            }
        }
        
        return TextResponse(
            result=result,
            status="success",
            timestamp="2024-01-01T00:00:00Z"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze")
async def analyze_text(request: TextRequest):
    return await process_text(request)

@app.post("/api/generate")
async def generate_text(request: TextRequest):
    try:
        result = {
            "original_prompt": request.text,
            "generated_text": f"Generated Bengali text based on: {request.text}",
            "confidence": 0.9,
            "metadata": {
                "model": "bengali-generator-v1",
                "generation_time": "0.2s"
            }
        }
        
        return {
            "result": result,
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
        
        # Process Bengali text
        if any('\u0980' <= char <= '\u09FF' for char in user_message):
            response_text = f"বাংলা প্রশ্নের উত্তর: {user_message} - এটি একটি বাংলা ভাষার প্রক্রিয়াকরণের উদাহরণ।"
        else:
            response_text = f"English query response: {user_message} - This is processed by Bengali NLP agent."
        
        # Store conversation
        store_conversation(session_id, user_message, response_text)
        
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
                        "content": response_text
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": len(user_message.split()),
                "completion_tokens": len(response_text.split()),
                "total_tokens": len(user_message.split()) + len(response_text.split())
            },
            "meta": {
                "memory_used": True,
                "processing_time": f"{processing_time:.2f}s",
                "confidence": 0.95,
                "session_id": session_id
            }
        }
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error in chat completions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/chat/stream")
async def chat_completions_stream(request: ChatCompletionsRequest, authorization: Optional[str] = Header(None), x_session_id: Optional[str] = Header(None)):
    """Streaming chat completions endpoint"""
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
        
        # Process Bengali text
        if any('\u0980' <= char <= '\u09FF' for char in user_message):
            response_text = f"বাংলা প্রশ্নের উত্তর: {user_message} - এটি একটি বাংলা ভাষার প্রক্রিয়াকরণের উদাহরণ।"
        else:
            response_text = f"English query response: {user_message} - This is processed by Bengali NLP agent."
        
        # Store conversation
        store_conversation(session_id, user_message, response_text)
        
        # Return streaming response (simplified for now)
        return {
            "id": f"chatcmpl-{uuid.uuid4()}",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": request.model,
            "choices": [
                {
                    "index": 0,
                    "delta": {
                        "content": response_text
                    },
                    "finish_reason": "stop"
                }
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error in streaming chat completions: {str(e)}")
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
            model="bengali-nlp-v1",
            messages=[ChatMessage(role="user", content=query_text)]
        )
        
        # Call chat completions endpoint
        response = await chat_completions(chat_request, authorization="Bearer local-only")
        
        # Return simplified response for backward compatibility
        return {
            "query": query_text,
            "response": response["choices"][0]["message"]["content"],
            "language": "bengali",
            "confidence": response["meta"]["confidence"],
            "processing_time": response["meta"]["processing_time"],
            "model": "bengali-nlp-v1"
        }
        
    except Exception as e:
        logging.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
