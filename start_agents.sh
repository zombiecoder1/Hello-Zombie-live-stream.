#!/bin/bash

# ZombieCoder Multi-Agent System Startup Script
# Safe startup with port checking and process management

echo "🚀 Starting ZombieCoder Multi-Agent System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -i :$port > /dev/null 2>&1; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to kill process on port
kill_port() {
    local port=$1
    local pids=$(lsof -ti :$port)
    if [ ! -z "$pids" ]; then
        echo -e "${YELLOW}Killing existing processes on port $port: $pids${NC}"
        kill -9 $pids
        sleep 1
    fi
}

# Function to start agent
start_agent() {
    local agent_name=$1
    local port=$2
    local script_path=$3
    
    echo -e "${BLUE}Starting $agent_name on port $port...${NC}"
    
    # Check and kill existing process on port
    if check_port $port; then
        kill_port $port
    fi
    
    # Start the agent in background
    cd /home/sahon/Desktop/Try/workspace
    source venv/bin/activate
    python $script_path &
    local agent_pid=$!
    
    # Wait a moment and check if it started successfully
    sleep 2
    if check_port $port; then
        echo -e "${GREEN}✅ $agent_name started successfully (PID: $agent_pid)${NC}"
        echo $agent_pid >> /tmp/zombiecoder_pids.txt
    else
        echo -e "${RED}❌ Failed to start $agent_name on port $port${NC}"
        return 1
    fi
}

# Clear PID file
> /tmp/zombiecoder_pids.txt

# Agent configurations
declare -A AGENTS=(
    ["Bengali NLP"]="8002:agents/bengali-nlp/main.py"
    ["Code Generation"]="8003:agents/code-generation/main.py"
    ["Code Review"]="8004:agents/code-review/main.py"
    ["Documentation"]="8005:agents/documentation/main.py"
    ["Testing"]="8006:agents/testing/main.py"
    ["Deployment"]="8007:agents/deployment/main.py"
    ["Voice Processor"]="8014:services/voice-processor/main.py"
)

# Start all agents
for agent_name in "${!AGENTS[@]}"; do
    IFS=':' read -r port script_path <<< "${AGENTS[$agent_name]}"
    start_agent "$agent_name" "$port" "$script_path"
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to start $agent_name. Stopping startup process.${NC}"
        exit 1
    fi
    sleep 1
done

# Start OpenAI Router Gateway
echo -e "${BLUE}Starting OpenAI Router Gateway on port 8001...${NC}"
if check_port 8001; then
    kill_port 8001
fi

cd /home/sahon/Desktop/Try/workspace
source venv/bin/activate
python zombie_openai_router.py &
gateway_pid=$!
echo $gateway_pid >> /tmp/zombiecoder_pids.txt

sleep 3
if check_port 8001; then
    echo -e "${GREEN}✅ OpenAI Router Gateway started successfully (PID: $gateway_pid)${NC}"
else
    echo -e "${RED}❌ Failed to start OpenAI Router Gateway${NC}"
    exit 1
fi

# Health check
echo -e "${BLUE}Performing health checks...${NC}"
sleep 2

# Check all agents
for agent_name in "${!AGENTS[@]}"; do
    IFS=':' read -r port script_path <<< "${AGENTS[$agent_name]}"
    if curl -s http://localhost:$port/health > /dev/null; then
        echo -e "${GREEN}✅ $agent_name health check passed${NC}"
    else
        echo -e "${RED}❌ $agent_name health check failed${NC}"
    fi
done

# Check gateway
if curl -s http://localhost:8001/health > /dev/null; then
    echo -e "${GREEN}✅ OpenAI Router Gateway health check passed${NC}"
else
    echo -e "${RED}❌ OpenAI Router Gateway health check failed${NC}"
fi

echo -e "${GREEN}🎉 All agents started successfully!${NC}"
echo -e "${BLUE}Available endpoints:${NC}"
echo -e "  • OpenAI Gateway: http://localhost:8001/v1"
echo -e "  • Bengali NLP: http://localhost:8002"
echo -e "  • Code Generation: http://localhost:8003"
echo -e "  • Code Review: http://localhost:8004"
echo -e "  • Documentation: http://localhost:8005"
echo -e "  • Testing: http://localhost:8006"
echo -e "  • Deployment: http://localhost:8007"
echo -e "  • Voice Processor: http://localhost:8014"

echo -e "${YELLOW}To stop all agents, run: ./stop_agents.sh${NC}"
