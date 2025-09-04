#!/bin/bash

# SecAgent Interactive Mode Launcher
# This script starts the interactive AI pentesting assistant

echo "🚀 Starting SecAgent Interactive Mode..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/installed" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    touch venv/installed
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env file with your API keys before running again."
    echo "   At minimum, you need either OPENAI_API_KEY or ANTHROPIC_API_KEY"
    exit 1
fi

# Start interactive agent
echo "🤖 Starting Interactive AI Pentesting Assistant..."
python3 interactive_agent.py
