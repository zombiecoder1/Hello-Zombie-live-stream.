#!/bin/bash

# ZombieCoder Multi-Agent System Stop Script

echo "🛑 Stopping ZombieCoder Multi-Agent System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to kill process on port
kill_port() {
    local port=$1
    local pids=$(lsof -ti :$port)
    if [ ! -z "$pids" ]; then
        echo -e "${YELLOW}Stopping processes on port $port: $pids${NC}"
        kill -9 $pids
        return 0
    else
        echo -e "${BLUE}No processes found on port $port${NC}"
        return 1
    fi
}

# Stop all agents
PORTS=(8001 8002 8003 8004 8005 8006 8007 8014)

for port in "${PORTS[@]}"; do
    kill_port $port
done

# Kill any remaining zombie processes
echo -e "${BLUE}Cleaning up any remaining processes...${NC}"
pkill -f "python.*main.py"
pkill -f "zombie_openai_router.py"

# Clean up PID file
if [ -f /tmp/zombiecoder_pids.txt ]; then
    rm /tmp/zombiecoder_pids.txt
fi

echo -e "${GREEN}✅ All agents stopped successfully!${NC}"
