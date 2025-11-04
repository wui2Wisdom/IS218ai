#!/bin/bash

# DupeFinder Startup Script
echo "🦝 Starting DupeFinder..."

# Navigate to project directory
cd /home/thewiseone/IS218/IS218ai

# Activate virtual environment
source .venv/bin/activate

# Export API key
export TAVILY_API_KEY=$(grep TAVILY_API_KEY .env | cut -d '=' -f2)

# Start backend
echo "Starting backend on port 8000..."
nohup uvicorn backend.app:app --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Check backend health
if curl -s http://localhost:8000/healthz | grep -q "ok"; then
    echo "✅ Backend is running (PID: $BACKEND_PID)"
else
    echo "❌ Backend failed to start"
    exit 1
fi

# Start frontend
echo "Starting frontend on port 5173..."
cd frontend
nohup python3 -m http.server 5173 > /dev/null 2>&1 &
FRONTEND_PID=$!

echo "✅ Frontend is running (PID: $FRONTEND_PID)"
echo ""
echo "🎉 DupeFinder is ready!"
echo "🌐 Open http://localhost:5173 in your browser"
echo ""
echo "To stop the servers:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
