#!/bin/bash

echo "🧟 ZombieCoder AI Development Platform"
echo "======================================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Start all services
echo "🚀 Starting all services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo "🔍 Checking service health..."

# Check API Gateway
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ API Gateway: Running"
else
    echo "❌ API Gateway: Not responding"
fi

# Check Web Portal
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Web Portal: Running"
else
    echo "❌ Web Portal: Not responding"
fi

# Check Ollama
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama: Running"
else
    echo "❌ Ollama: Not responding"
fi

echo ""
echo "🎉 ZombieCoder platform is ready!"
echo "🌐 Web Portal: http://localhost:3000"
echo "🔌 API Gateway: http://localhost:8000"
echo "🤖 Ollama: http://localhost:11434"
echo ""
echo "To stop all services: docker-compose down"
