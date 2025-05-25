#!/bin/bash

# Script to start both API and UI development servers

# Terminal colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting SEO Agent development servers...${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python 3 is required but not found. Please install Python 3.${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}Node.js is required but not found. Please install Node.js.${NC}"
    exit 1
fi

# Check if the API directory exists
if [ ! -d "api" ]; then
    echo -e "${YELLOW}API directory not found. Make sure you're running this script from the project root.${NC}"
    exit 1
fi

# Check if the frontend directory exists
if [ ! -d "frontend" ]; then
    echo -e "${YELLOW}Frontend directory not found. Make sure you're running this script from the project root.${NC}"
    exit 1
fi

# Check if .env file exists, create if not
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    echo "OPENAI_API_KEY=your-openai-key" > .env
    echo "SERPAPI_KEY=your-serpapi-key" >> .env
    echo "AHREFS_API_KEY=your-ahrefs-key" >> .env
    echo "SEMRUSH_API_KEY=your-semrush-key" >> .env
    echo -e "${YELLOW}Please update the .env file with your API keys.${NC}"
fi

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Start API server in background
echo -e "${GREEN}Starting FastAPI server...${NC}"
cd api
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi
python3 -m uvicorn main:app --reload --port 8000 &
API_PID=$!
cd ..

# Wait a moment for the API to start
sleep 2

# Start frontend server in background
echo -e "${GREEN}Starting Next.js frontend...${NC}"
cd frontend
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Installing frontend dependencies...${NC}"
    npm install
fi
npm run dev &
UI_PID=$!
cd ..

# Wait for both servers
echo -e "${GREEN}Both servers are running!${NC}"
echo -e "${BLUE}API: http://localhost:8000${NC}"
echo -e "${BLUE}UI: http://localhost:3000${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}"

# Trap SIGINT to kill both processes
trap "kill $API_PID $UI_PID; exit" INT

# Wait for either process to exit
wait
