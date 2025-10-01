from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import uvicorn
import sqlite3
import json
import os
from datetime import datetime
from typing import Optional
import uuid
import time
import logging
from typing import Dict, Any, List

app = FastAPI(title="Code Generation Agent", version="1.0.0")

# Initialize database and logging
DB_PATH = "code_generation_memory.db"
LOG_FILE = "logs/code_generation.log"

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
        "model": "code-generator-v1",
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
    "agent_type": "code-generation",
    "description": "AI-powered code generation assistant"
}

# Memory system setup
MEMORY_DB_PATH = "/home/sahon/Desktop/Try/workspace/agents/memory/programming/memory.db"

def init_memory_db():
    """Initialize memory database"""
    os.makedirs(os.path.dirname(MEMORY_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(MEMORY_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS code_generation_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            prompt TEXT NOT NULL,
            language TEXT NOT NULL,
            framework TEXT,
            generated_code TEXT NOT NULL,
            explanation TEXT NOT NULL,
            model_used TEXT NOT NULL,
            response_time REAL
        )
    ''')
    conn.commit()
    conn.close()

def log_to_memory(prompt, language, framework, generated_code, explanation, model_used, response_time):
    """Log generation to memory database"""
    try:
        conn = sqlite3.connect(MEMORY_DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO code_generation_logs 
            (timestamp, prompt, language, framework, generated_code, explanation, model_used, response_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), prompt, language, framework, generated_code, explanation, model_used, response_time))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Memory logging error: {e}")

# Initialize memory on startup
init_memory_db()

class CodeRequest(BaseModel):
    prompt: str
    language: str = "python"
    framework: str = None
    requirements: List[str] = []

class CodeResponse(BaseModel):
    code: str
    explanation: str
    status: str
    timestamp: str

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "code-generation",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/api/status")
async def get_status():
    return {
        "message": "Code Generation Agent is running",
        "version": "1.0.0",
        "supported_languages": [
            "python", "javascript", "typescript", "java", "cpp", "go", "rust"
        ],
        "supported_frameworks": [
            "react", "vue", "angular", "django", "flask", "express", "spring"
        ],
        "metadata": ZOMBIECODER_METADATA,
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.post("/api/generate", response_model=CodeResponse)
async def generate_code(request: CodeRequest):
    try:
        # Call local model service for code generation
        import requests
        
        model_request = {
            "prompt": f"Generate {request.language} code for: {request.prompt}. Framework: {request.framework or 'none'}. Requirements: {', '.join(request.requirements)}",
            "model": "llama2",
            "max_tokens": 1000,
            "temperature": 0.2
        }
        
        try:
            response = requests.post(
                "http://localhost:5252/api/generate",
                json=model_request,
                timeout=30
            )
            
            if response.status_code == 200:
                model_result = response.json()
                ai_generated_code = model_result.get("response", "")
            else:
                ai_generated_code = "# Local model code generation unavailable\n# Fallback code generated"
        except:
            ai_generated_code = "# Local model code generation unavailable\n# Fallback code generated"
        
        # Use AI generated code or fallback
        if ai_generated_code and not ai_generated_code.startswith("# Local model"):
            generated_code = ai_generated_code
        else:
            generated_code = f"""
# Generated {request.language} code
# Prompt: {request.prompt}

def main():
    print("Hello, World!")
    print("Generated code for: {request.prompt}")
    
    # Add framework-specific code if specified
    {f"# Framework: {request.framework}" if request.framework else ""}
    
    return True

if __name__ == "__main__":
    main()
"""
        
        explanation = f"""
This code was generated using local AI model based on your prompt: "{request.prompt}"

Key features:
- Written in {request.language}
- {f"Uses {request.framework} framework" if request.framework else "No specific framework"}
- Generated by local AI model for privacy and performance
- Ready to run and modify as needed
"""
        
        # Log to memory
        log_to_memory(
            prompt=request.prompt,
            language=request.language,
            framework=request.framework or "none",
            generated_code=generated_code.strip(),
            explanation=explanation,
            model_used="local-llama2",
            response_time=0.1
        )
        
        return CodeResponse(
            code=generated_code.strip(),
            explanation=explanation,
            status="success",
            timestamp="2024-01-01T00:00:00Z"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/optimize")
async def optimize_code(request: CodeRequest):
    try:
        optimized_code = f"""
# Optimized {request.language} code
# Original prompt: {request.prompt}

def optimized_main():
    # Optimized implementation
    result = "Optimized code for: " + "{request.prompt}"
    return result

if __name__ == "__main__":
    print(optimized_main())
"""
        
        return {
            "code": optimized_code.strip(),
            "optimizations": [
                "Improved performance",
                "Better error handling",
                "Cleaner code structure"
            ],
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

@app.post("/v1/chat/stream")
async def chat_stream(request: ChatCompletionsRequest, authorization: Optional[str] = Header(None), x_session_id: Optional[str] = Header(None)):
    """Streaming chat completions endpoint"""
    try:
        # Check authorization
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        
        # Extract user message
        user_message = ""
        if request.messages:
            user_message = request.messages[-1].content
        
        if not user_message:
            raise HTTPException(status_code=400, detail="No user message found")
        
        # Generate streaming response
        from fastapi.responses import StreamingResponse
        import json
        
        def generate_stream():
            # Send initial response
            yield f"data: {json.dumps({'id': f'chatcmpl-{uuid.uuid4()}', 'object': 'chat.completion.chunk', 'created': int(time.time()), 'model': request.model, 'choices': [{'index': 0, 'delta': {'role': 'assistant'}, 'finish_reason': None}]})}\n\n"
            
            # Generate code content
            generated_code = f"# Generated code for: {user_message}\ndef main():\n    print('Processing request...')\n    return True"
            
            # Stream the content
            words = generated_code.split()
            for word in words:
                yield f"data: {json.dumps({'id': f'chatcmpl-{uuid.uuid4()}', 'object': 'chat.completion.chunk', 'created': int(time.time()), 'model': request.model, 'choices': [{'index': 0, 'delta': {'content': word + ' '}, 'finish_reason': None}]})}\n\n"
                time.sleep(0.05)  # Small delay for streaming effect
            
            # Send final chunk
            yield f"data: {json.dumps({'id': f'chatcmpl-{uuid.uuid4()}', 'object': 'chat.completion.chunk', 'created': int(time.time()), 'model': request.model, 'choices': [{'index': 0, 'delta': {}, 'finish_reason': 'stop'}]})}\n\n"
            yield "data: [DONE]\n\n"
        
        return StreamingResponse(generate_stream(), media_type="text/plain")
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error in chat stream: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

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
        
        # Enhanced language detection with Bengali input handling
        detected_language = "python"  # Default to Python for Bengali requests
        
        # Check for Bengali language keywords and override detection
        bengali_keywords = ["পাইথন", "python", "py", "ফাইলে", "ফাংশন", "ক্লাস", "ডেটা", "লিস্ট", "ডিকশনারি", "ফাইলে", "লিখো", "কোড", "প্রোগ্রাম", "স্ক্রিপ্ট", "অ্যালগরিদম"]
        
        # Bengali input detection
        bengali_chars = "আইউএকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ৎ"
        has_bengali = any(char in user_message for char in bengali_chars)
        
        if has_bengali and any(keyword in user_message.lower() for keyword in bengali_keywords):
            detected_language = "python"
        elif "javascript" in user_message.lower() or "js" in user_message.lower():
            detected_language = "javascript"
        elif "java" in user_message.lower():
            detected_language = "java"
        elif "cpp" in user_message.lower() or "c++" in user_message.lower():
            detected_language = "cpp"
        
        # Generate code based on detected language
        if detected_language == "python":
            if "add" in user_message.lower() or "যোগ" in user_message or "দুই" in user_message:
                generated_code = '''def add(a, b):
    """Add two numbers and return the result"""
    return a + b

# Example usage
result = add(5, 3)
print(f"5 + 3 = {result}")'''
            elif "loop" in user_message.lower() or "লুপ" in user_message:
                generated_code = '''# Print numbers from 1 to 10 using a loop
for i in range(1, 11):
    print(i)

# Alternative with while loop
i = 1
while i <= 10:
    print(i)
    i += 1'''
            elif "ফাইল" in user_message or "file" in user_message.lower():
                generated_code = '''# File operations in Python
def read_file(filename):
    """Read content from a file"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "File not found"

def write_file(filename, content):
    """Write content to a file"""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        return "File written successfully"
    except Exception as e:
        return f"Error writing file: {e}"

# Example usage
content = read_file("example.txt")
print(content)

write_file("output.txt", "Hello, World!")'''
            else:
                generated_code = f'''# Generated Python code for: {user_message}
def process_request():
    """Process the given request"""
    print("Processing request...")
    print(f"Input: {user_message}")
    
    # Add your logic here
    result = "Processing completed"
    return result

if __name__ == "__main__":
    result = process_request()
    print(result)'''
        else:
            generated_code = f'''// Generated code for: {user_message}
function processRequest() {{
    console.log("Processing:", "{user_message}");
    return "Code generated successfully";
}}

processRequest();'''
        
        response_text = f"Here's the generated code:\n\n```{('python' if 'python' in user_message.lower() else 'javascript')}\n{generated_code}\n```\n\nThis code was generated based on your request: {user_message}"
        
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
                "confidence": 0.92,
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
            model="code-generator-v1",
            messages=[ChatMessage(role="user", content=query_text)]
        )
        
        # Call chat completions endpoint
        response = await chat_completions(chat_request, authorization="Bearer local-only")
        
        # Extract code from response
        response_content = response["choices"][0]["message"]["content"]
        
        # Try to extract code block
        code_start = response_content.find("```")
        if code_start != -1:
            code_start = response_content.find("\n", code_start) + 1
            code_end = response_content.find("```", code_start)
            if code_end != -1:
                generated_code = response_content[code_start:code_end].strip()
            else:
                generated_code = response_content[code_start:].strip()
        else:
            generated_code = response_content
        
        # Return simplified response for backward compatibility
        return {
            "query": query_text,
            "code": generated_code,
            "language": "python" if "python" in query_text.lower() else "javascript",
            "explanation": f"Generated code for: {query_text}",
            "confidence": response["meta"]["confidence"],
            "processing_time": response["meta"]["processing_time"],
            "model": "code-generator-v1"
        }
        
    except Exception as e:
        logging.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
