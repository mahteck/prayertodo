#!/bin/bash
# SalaatFlow Chatbot Startup Script
# This script starts the backend server for the chatbot

echo "🤖 Starting SalaatFlow Chatbot Backend..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found!"
    echo "Please create it first: python -m venv venv"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create .env file with your configuration"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if GEMINI_API_KEY is set
if ! grep -q "GEMINI_API_KEY=AIza" .env; then
    echo "⚠️  Warning: GEMINI_API_KEY may not be set correctly in .env"
    echo "   Make sure it starts with 'AIza'"
fi

# Create logs directory if it doesn't exist
if [ ! -d "logs" ]; then
    mkdir -p logs
    echo "📂 Created logs directory"
fi

# Start the server
echo "🚀 Starting FastAPI server on http://0.0.0.0:8000..."
echo ""
echo "📝 Logs will be written to:"
echo "   - logs/chatbot.log (all activity)"
echo "   - logs/chatbot_errors.log (errors only)"
echo ""
echo "🔍 Health check: http://localhost:8000/api/v1/chat/health"
echo "💬 Chat endpoint: http://localhost:8000/api/v1/chat/"
echo ""
echo "Press CTRL+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start uvicorn with auto-reload
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
