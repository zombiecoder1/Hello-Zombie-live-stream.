#!/usr/bin/env python3
"""
ZombieCoder OpenAI Router Gateway
Unified OpenAI-compatible API for all agents (8002-8007, 8014)
"""

import asyncio
import json
import logging
import time
import uuid
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException, Header, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Agent Configuration
AGENTS = {
    "bengali_nlp": {"url": "http://127.0.0.1:8002", "name": "Bengali NLP", "type": "language"},
    "code_generation": {"url": "http://127.0.0.1:8003", "name": "Code Generation", "type": "coding"},
    "code_review": {"url": "http://127.0.0.1:8004", "name": "Code Review", "type": "coding"},
    "documentation": {"url": "http://127.0.0.1:8005", "name": "Documentation", "type": "writing"},
    "testing": {"url": "http://127.0.0.1:8006", "name": "Testing", "type": "coding"},
    "deployment": {"url": "http://127.0.0.1:8007", "name": "Deployment", "type": "infrastructure"},
    "voice_processor": {"url": "http://127.0.0.1:8014", "name": "Voice Processor", "type": "audio"}
}

# OpenAI-compatible Models
OPENAI_MODELS = {
    "gpt-3.5-turbo": "bengali_nlp",
    "gpt-4": "bengali_nlp", 
    "gpt-4-turbo": "bengali_nlp",
    "codex": "code_generation",
    "davinci-codex": "code_generation",
    "claude-instant": "documentation",
    "claude": "documentation",
    "tts-1": "voice_processor",
    "whisper-1": "voice_processor"
}

app = FastAPI(
    title="ZombieCoder OpenAI Gateway",
    description="Unified OpenAI-compatible API for Multi-Agent System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionsRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    stream: Optional[bool] = False
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000
    top_p: Optional[float] = 1.0
    frequency_penalty: Optional[float] = 0.0
    presence_penalty: Optional[float] = 0.0

class AudioSpeechRequest(BaseModel):
    model: str = "tts-1"
    input: str
    voice: str = "alloy"
    response_format: str = "mp3"
    speed: float = 1.0

async def route_to_agent(model: str, messages: List[ChatMessage]) -> tuple[str, str]:
    """Route request to appropriate agent based on model and content"""
    
    # Direct model mapping
    if model in OPENAI_MODELS:
        agent_key = OPENAI_MODELS[model]
        return agent_key, AGENTS[agent_key]["url"]
    
    # Content-based routing
    content = " ".join([msg.content for msg in messages if msg.role == "user"])
    content_lower = content.lower()
    
    # Bengali language detection
    bengali_chars = "আইউএকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ৎ"
    if any(char in content for char in bengali_chars):
        return "bengali_nlp", AGENTS["bengali_nlp"]["url"]
    
    # Code-related keywords
    code_keywords = ["function", "class", "def", "import", "code", "program", "script", "algorithm"]
    if any(keyword in content_lower for keyword in code_keywords):
        return "code_generation", AGENTS["code_generation"]["url"]
    
    # Review keywords
    review_keywords = ["review", "check", "analyze", "security", "bug", "error", "fix"]
    if any(keyword in content_lower for keyword in review_keywords):
        return "code_review", AGENTS["code_review"]["url"]
    
    # Documentation keywords
    doc_keywords = ["documentation", "doc", "readme", "api", "guide", "manual", "tutorial"]
    if any(keyword in content_lower for keyword in doc_keywords):
        return "documentation", AGENTS["documentation"]["url"]
    
    # Testing keywords
    test_keywords = ["test", "unit test", "pytest", "assert", "mock", "coverage"]
    if any(keyword in content_lower for keyword in test_keywords):
        return "testing", AGENTS["testing"]["url"]
    
    # Deployment keywords
    deploy_keywords = ["deploy", "docker", "kubernetes", "server", "production", "infrastructure"]
    if any(keyword in content_lower for keyword in deploy_keywords):
        return "deployment", AGENTS["deployment"]["url"]
    
    # Voice/Audio keywords
    audio_keywords = ["speech", "audio", "voice", "sound", "tts", "text-to-speech"]
    if any(keyword in content_lower for keyword in audio_keywords):
        return "voice_processor", AGENTS["voice_processor"]["url"]
    
    # Default to Bengali NLP for general queries
    return "bengali_nlp", AGENTS["bengali_nlp"]["url"]

async def call_agent(agent_url: str, payload: dict, headers: dict) -> dict:
    """Call individual agent with error handling"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{agent_url}/v1/chat/completions",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Agent {agent_url} returned {response.status_code}: {response.text}")
                return {
                    "error": f"Agent error: {response.status_code}",
                    "details": response.text
                }
    except httpx.TimeoutException:
        logger.error(f"Timeout calling agent {agent_url}")
        return {"error": "Agent timeout", "details": "Request timed out"}
    except Exception as e:
        logger.error(f"Error calling agent {agent_url}: {str(e)}")
        return {"error": "Agent communication error", "details": str(e)}

@app.get("/v1/models")
async def list_models():
    """List available models"""
    return {
        "object": "list",
        "data": [
            {
                "id": model,
                "object": "model",
                "created": int(time.time()),
                "owned_by": "zombiecoder",
                "permission": [],
                "root": model,
                "parent": None
            }
            for model in OPENAI_MODELS.keys()
        ]
    }

@app.post("/v1/chat/completions")
async def chat_completions(
    request: ChatCompletionsRequest,
    authorization: Optional[str] = Header(None),
    x_session_id: Optional[str] = Header(None)
):
    """OpenAI-compatible chat completions endpoint"""
    try:
        # Check authorization
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        
        # Route to appropriate agent
        agent_key, agent_url = await route_to_agent(request.model, request.messages)
        
        logger.info(f"Routing request to {agent_key} ({agent_url})")
        
        # Prepare headers for agent call
        headers = {
            "Content-Type": "application/json",
            "Authorization": authorization,
        }
        if x_session_id:
            headers["X-Session-ID"] = x_session_id
        
        # Prepare payload for agent
        payload = {
            "model": request.model,
            "messages": [{"role": msg.role, "content": msg.content} for msg in request.messages],
            "stream": request.stream,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "top_p": request.top_p,
            "frequency_penalty": request.frequency_penalty,
            "presence_penalty": request.presence_penalty
        }
        
        # Call agent
        agent_response = await call_agent(agent_url, payload, headers)
        
        if "error" in agent_response:
            raise HTTPException(status_code=500, detail=agent_response["error"])
        
        # Add gateway metadata
        if "meta" not in agent_response:
            agent_response["meta"] = {}
        
        agent_response["meta"]["gateway"] = True
        agent_response["meta"]["routed_to"] = agent_key
        agent_response["meta"]["agent_url"] = agent_url
        
        return agent_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Gateway error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/audio/speech")
async def audio_speech(
    request: AudioSpeechRequest,
    authorization: Optional[str] = Header(None)
):
    """OpenAI-compatible audio speech endpoint"""
    try:
        # Check authorization
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        
        # Route to voice processor
        agent_url = AGENTS["voice_processor"]["url"]
        
        # Prepare headers and payload
        headers = {
            "Content-Type": "application/json",
            "Authorization": authorization
        }
        
        payload = {
            "model": request.model,
            "input": request.input,
            "voice": request.voice,
            "response_format": request.response_format,
            "speed": request.speed
        }
        
        # Call voice processor
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{agent_url}/v1/audio/speech",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Audio gateway error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    health_status = {"status": "healthy", "gateway": "zombiecoder", "timestamp": time.time()}
    
    # Check all agents
    for agent_key, agent_info in AGENTS.items():
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{agent_info['url']}/health")
                health_status[agent_key] = "healthy" if response.status_code == 200 else "unhealthy"
        except:
            health_status[agent_key] = "unreachable"
    
    return health_status

@app.get("/agents")
async def list_agents():
    """List all available agents"""
    return {
        "agents": AGENTS,
        "models": OPENAI_MODELS,
        "total_agents": len(AGENTS),
        "total_models": len(OPENAI_MODELS)
    }

if __name__ == "__main__":
    print("🚀 Starting ZombieCoder OpenAI Gateway...")
    print(f"📡 Available Agents: {len(AGENTS)}")
    print(f"🤖 Available Models: {len(OPENAI_MODELS)}")
    print("🔗 OpenAI API Base: http://127.0.0.1:8001/v1")
    print("📋 Models: http://127.0.0.1:8001/v1/models")
    print("💬 Chat: http://127.0.0.1:8001/v1/chat/completions")
    print("🎵 Audio: http://127.0.0.1:8001/v1/audio/speech")
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
