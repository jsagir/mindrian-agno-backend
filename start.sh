#!/bin/bash
# Start Mindrian AgentOS

echo "================================================"
echo "       MINDRIAN AGENT OS - STARTUP"
echo "================================================"
echo ""

# Check for .env file
if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    echo "Please copy .env.example to .env and fill in your API keys:"
    echo "  cp .env.example .env"
    echo ""
    exit 1
fi

# Source environment
export $(grep -v '^#' .env | xargs)

# Check required API keys
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "WARNING: ANTHROPIC_API_KEY not set in .env"
fi

if [ -z "$PINECONE_API_KEY" ]; then
    echo "WARNING: PINECONE_API_KEY not set in .env"
fi

echo "Starting Mindrian AgentOS on port 7777..."
echo ""
echo "Connect Agent UI at: http://localhost:3000"
echo "API Docs at: http://localhost:7777/docs"
echo ""

# Start the server
python mindrian_os.py
