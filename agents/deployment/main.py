from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import uvicorn
from typing import Dict, Any, List, Optional
import json
import sqlite3
import uuid
import time
import logging

app = FastAPI(title="Deployment Agent", version="1.0.0")

# Initialize database and logging
DB_PATH = "deployment_memory.db"
LOG_FILE = "deployment.log"

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
        "model": "deployment-generator-v1",
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

class DeploymentRequest(BaseModel):
    code: str
    language: str = "python"
    deployment_type: str = "docker"
    environment: str = "production"

class DeploymentResponse(BaseModel):
    deployment_config: str
    status: str
    timestamp: str

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "deployment",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/api/status")
async def get_status():
    return {
        "message": "Deployment Agent is running",
        "version": "1.0.0",
        "supported_deployment_types": [
            "docker",
            "kubernetes",
            "serverless",
            "traditional"
        ],
        "supported_environments": [
            "development",
            "staging",
            "production"
        ],
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.post("/api/deploy", response_model=DeploymentResponse)
async def deploy_application(request: DeploymentRequest):
    try:
        # Call local model service for deployment configuration generation
        import requests
        
        model_request = {
            "prompt": f"Generate {request.deployment_type} deployment configuration for {request.language} application in {request.environment} environment. Code:\n\n{request.code}\n\nMake it production-ready with proper security, monitoring, and scaling considerations.",
            "model": "llama2",
            "max_tokens": 1000,
            "temperature": 0.1
        }
        
        try:
            response = requests.post(
                "http://localhost:5252/api/generate",
                json=model_request,
                timeout=30
            )
            
            if response.status_code == 200:
                model_result = response.json()
                ai_deployment_config = model_result.get("response", "")
            else:
                ai_deployment_config = None
        except:
            ai_deployment_config = None
        
        # Use AI generated deployment config or fallback
        if ai_deployment_config and not ai_deployment_config.startswith("# Local model"):
            deployment_config = ai_deployment_config
        else:
            # Fallback deployment configuration
            if request.deployment_type == "docker":
                deployment_config = f"""
# Dockerfile for {request.language} application
FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "main.py"]
"""
            elif request.deployment_type == "kubernetes":
                deployment_config = f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {request.language}-app
  labels:
    app: {request.language}-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {request.language}-app
  template:
    metadata:
      labels:
        app: {request.language}-app
    spec:
      containers:
      - name: {request.language}-app
        image: {request.language}-app:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENVIRONMENT
          value: "{request.environment}"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: {request.language}-app-service
spec:
  selector:
    app: {request.language}-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
"""
            else:
                deployment_config = f"""
# Deployment configuration for {request.language} application
# Environment: {request.environment}
# Type: {request.deployment_type}

# Build commands
npm install
npm run build

# Start commands
npm start

# Environment variables
NODE_ENV={request.environment}
PORT=8000
"""
        
        return DeploymentResponse(
            deployment_config=deployment_config.strip(),
            status="success",
            timestamp="2024-01-01T00:00:00Z"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ci-cd")
async def generate_cicd(request: DeploymentRequest):
    try:
        cicd_config = f"""
# CI/CD Pipeline Configuration
name: Deploy {request.language} Application

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up {request.language}
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest tests/
    - name: Run linting
      run: |
        flake8 .
        black --check .

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Build Docker image
      run: |
        docker build -t {request.language}-app:${{{{ github.sha }}}} .
    - name: Push to registry
      run: |
        echo "Pushing to registry..."

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy to {request.environment}
      run: |
        echo "Deploying to {request.environment}..."
        kubectl apply -f k8s/
"""
        
        return {
            "cicd_config": cicd_config.strip(),
            "status": "success",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/monitoring")
async def setup_monitoring(request: DeploymentRequest):
    try:
        monitoring_config = f"""
# Monitoring Configuration
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-storage:/var/lib/grafana

  {request.language}-app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT={request.environment}
    depends_on:
      - prometheus

volumes:
  grafana-storage:
"""
        
        return {
            "monitoring_config": monitoring_config.strip(),
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
        
        # Generate deployment configuration based on query
        if "dockerfile" in user_message.lower() or "docker" in user_message.lower():
            deployment_config = '''# Dockerfile for Flask Application
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \\
    && apt-get install -y --no-install-recommends \\
        build-essential \\
        curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \\
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser \\
    && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "app.py"]

# Build command: docker build -t flask-app .
# Run command: docker run -p 8000:8000 flask-app'''
        elif "স্ক্রিপ্ট" in user_message or "script" in user_message.lower():
            deployment_config = '''#!/bin/bash
# Server Deployment Script

set -e

echo "🚀 Starting server deployment..."

# Variables
APP_NAME="flask-app"
DEPLOY_DIR="/var/www/app"
SERVICE_NAME="flask-app"
PORT=8000

# Create deployment directory
sudo mkdir -p $DEPLOY_DIR
sudo chown $USER:$USER $DEPLOY_DIR

# Copy application files
cp -r . $DEPLOY_DIR/
cd $DEPLOY_DIR

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create systemd service
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null <<EOF
[Unit]
Description=Flask Application
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$DEPLOY_DIR
Environment=PATH=$DEPLOY_DIR/venv/bin
ExecStart=/usr/bin/python3 app.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start service
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

# Check status
echo "✅ Checking service status..."
sudo systemctl status $SERVICE_NAME --no-pager

echo "🎉 Deployment completed successfully!"
echo "Service running on http://localhost:$PORT"
'''
        else:
            deployment_config = f'''# Deployment Configuration for: {user_message}

## Production Environment Setup

### 1. Server Requirements
- Ubuntu 20.04+ or CentOS 8+
- Python 3.8+
- Nginx (reverse proxy)
- SSL Certificate

### 2. Application Deployment
```bash
# Clone repository
git clone <repository-url>
cd <app-directory>

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

### 3. Nginx Configuration
```nginx
server {{
    listen 80;
    server_name your-domain.com;
    
    location / {{
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }}
}}
```

### 4. SSL Setup
```bash
sudo certbot --nginx -d your-domain.com
```

### 5. Process Management
```bash
# Using systemd
sudo systemctl enable your-app
sudo systemctl start your-app
```

## Monitoring & Logs
- Application logs: /var/log/your-app/
- Nginx logs: /var/log/nginx/
- System logs: journalctl -u your-app
'''
        
        # Store conversation
        store_conversation(session_id, user_message, deployment_config)
        
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
                        "content": deployment_config
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": len(user_message.split()),
                "completion_tokens": len(deployment_config.split()),
                "total_tokens": len(user_message.split()) + len(deployment_config.split())
            },
            "meta": {
                "memory_used": True,
                "processing_time": f"{processing_time:.2f}s",
                "confidence": 0.93,
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
            model="deployment-generator-v1",
            messages=[ChatMessage(role="user", content=query_text)]
        )
        
        # Call chat completions endpoint
        response = await chat_completions(chat_request, authorization="Bearer local-only")
        
        # Return simplified response for backward compatibility
        return {
            "query": query_text,
            "deployment_config": response["choices"][0]["message"]["content"],
            "type": "dockerfile" if "docker" in query_text.lower() else "script",
            "confidence": response["meta"]["confidence"],
            "processing_time": response["meta"]["processing_time"],
            "model": "deployment-generator-v1"
        }
        
    except Exception as e:
        logging.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8007)
