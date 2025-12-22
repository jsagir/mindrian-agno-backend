#!/bin/bash
# Set up Agent UI Frontend for Mindrian

echo "================================================"
echo "       MINDRIAN AGENT UI SETUP"
echo "================================================"
echo ""

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "ERROR: npm is not installed"
    echo "Please install Node.js and npm first"
    exit 1
fi

echo "Creating Agent UI frontend..."
echo ""

# Create Agent UI project
npx create-agent-ui@latest mindrian-frontend

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create Agent UI project"
    exit 1
fi

cd mindrian-frontend

# Create .env.local for Agent UI
cat > .env.local << EOF
# Mindrian Agent UI Configuration
# Default connection to AgentOS on port 7777
NEXT_PUBLIC_AGENT_OS_URL=http://localhost:7777
EOF

echo ""
echo "================================================"
echo "       SETUP COMPLETE!"
echo "================================================"
echo ""
echo "To start Mindrian:"
echo ""
echo "1. Terminal 1 - Start AgentOS (backend):"
echo "   cd mindrian-agno-ui"
echo "   ./start.sh"
echo ""
echo "2. Terminal 2 - Start Agent UI (frontend):"
echo "   cd mindrian-frontend"
echo "   npm run dev"
echo ""
echo "3. Open http://localhost:3000"
echo "4. Connect to http://localhost:7777"
echo ""
echo "================================================"
