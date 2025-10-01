# OpenAI-compatible Chat Completions endpoint template

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import uvicorn
from typing import Dict, Any, Optional
import json
import sqlite3
import uuid
import time
import logging

# Initialize database and logging
DB_PATH = "agent_memory.db"
LOG_FILE = "agent.log"

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
        "model": "agent-v1",
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

# OpenAI-compatible Chat Completions endpoint
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionsRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    stream: Optional[bool] = False

def create_chat_completions_endpoint(app, agent_name: str, process_function):
    """Create OpenAI-compatible chat completions endpoint for any agent"""
    
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
            
            # Process using agent-specific function
            response_text = process_function(user_message)
            
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

def create_proxy_query_endpoint(app, agent_name: str, process_function):
    """Create proxy query endpoint that uses chat completions"""
    
    @app.post("/query")
    async def query_endpoint(request: dict):
        """Query endpoint for testing compatibility - proxies to chat completions"""
        try:
            query_text = request.get("query", "")
            
            # Create chat completions request
            chat_request = ChatCompletionsRequest(
                model=f"{agent_name}-v1",
                messages=[ChatMessage(role="user", content=query_text)]
            )
            
            # Call chat completions endpoint
            response = await chat_completions(chat_request, authorization="Bearer local-only")
            
            # Return simplified response for backward compatibility
            return {
                "query": query_text,
                "response": response["choices"][0]["message"]["content"],
                "confidence": response["meta"]["confidence"],
                "processing_time": response["meta"]["processing_time"],
                "model": f"{agent_name}-v1"
            }
            
        except Exception as e:
            logging.error(f"Error processing query: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
