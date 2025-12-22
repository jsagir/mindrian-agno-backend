# Mindrian AgentOS

AI-Powered Innovation Platform using Agno Framework and Agent UI.

## Overview

Mindrian is a thinking partner platform that helps with innovation methodology. It features:

- **7 Larry Roles**: Clarifier, Coach, Teacher, PWS Instructor, Devil's Advocate, Synthesizer, Expert
- **PWS Brain**: RAG integration with 1,371 PWS course records via Pinecone
- **Agent Teams**: Coordinated multi-agent workflows
- **Agent UI**: Modern chat interface (no Syncfusion)

## Quick Start

### 1. Install Dependencies

```bash
cd mindrian-agno-ui
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

Required keys:
- `GOOGLE_AI_API_KEY` - For Gemini 3 LLM
- `PINECONE_API_KEY` - For PWS Brain RAG

### 3. Start AgentOS (Port 7777)

```bash
./start.sh
# Or: python mindrian_os.py
```

### 4. Start Agent UI (Port 3000)

In a new terminal:

```bash
npx create-agent-ui@latest mindrian-frontend
cd mindrian-frontend
npm run dev
```

Then open http://localhost:3000 and connect to http://localhost:7777

## Architecture

```
mindrian-agno-ui/
├── mindrian_os.py          # Main AgentOS entry point (port 7777)
├── agents/
│   └── larry.py            # All 7 Larry agent roles
├── teams/
│   ├── clarification.py    # Clarifier + Devil + Synthesizer
│   └── analysis.py         # PWS Instructor + Expert + Coach
├── prompts/
│   └── larry_prompts.py    # System prompts for all roles
├── tools/
│   └── pws_brain.py        # Pinecone RAG tools
└── config/
    └── settings.py         # Configuration management
```

## Larry Roles

| Role | Icon | Purpose |
|------|------|---------|
| Clarifier | 🔍 | Asks questions to understand (max 5) |
| Coach | 🧭 | Step-by-step framework guidance |
| Teacher | 🎓 | Deep-dive education on concepts |
| PWS Instructor | 🎯 | Hands-on methodology implementation |
| Devil's Advocate | 😈 | Challenge assumptions |
| Synthesizer | 📊 | Organize into SCQA structure |
| Expert | 🧠 | Domain knowledge application |

## PWS Brain Integration

The PWS Brain contains 1,371 indexed course records covering:

- Jobs to Be Done (JTBD)
- Minto Pyramid / SCQA
- S-Curve Analysis
- Four Lenses of Innovation
- White Space Mapping
- Scenario Analysis
- PWS Validation Framework

Agents automatically search this knowledge to ground responses in methodology.

## Teams

### Clarification Team
Sequential workflow: Clarifier → Devil → Synthesizer

### Analysis Team
Collaborative: PWS Instructor + Expert + Coach work together

## API Endpoints

- `GET /` - API info and agent list
- `GET /health` - Health check
- `GET /docs` - OpenAPI documentation

Agent UI handles chat via the Agno protocol on port 7777.

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check .
```

## Replit Deployment (Share with Others!)

This project is Replit-ready for easy sharing:

### Backend (AgentOS)

1. **Create Replit**: Go to [replit.com](https://replit.com) → Create Repl → Import from GitHub
2. **Upload Files**: Upload the `mindrian-agno-ui` folder (or connect your GitHub repo)
3. **Add Secrets** (lock icon in sidebar):
   - `GOOGLE_AI_API_KEY` - Get from [Google AI Studio](https://aistudio.google.com/apikey)
   - `PINECONE_API_KEY` - Get from [Pinecone Console](https://app.pinecone.io)
4. **Click Run** - AgentOS starts on the Replit URL

### Frontend (Agent UI)

1. **Create separate Replit**: Import the `mindrian-frontend` folder
2. **Add Secret**:
   - `NEXT_PUBLIC_AGENT_OS_URL` = Your backend Replit URL (e.g., `https://your-repl.username.repl.co`)
3. **Click Run** - UI connects to your AgentOS

### Share Your Mindrian

Once deployed, share these URLs:
- **Backend API**: `https://your-backend.username.repl.co`
- **Frontend UI**: `https://your-frontend.username.repl.co`

Anyone with the frontend URL can use your Mindrian agents!

### Quick Deploy Checklist

| Secret | Required | Where to Get |
|--------|----------|--------------|
| `GOOGLE_AI_API_KEY` | Yes | [Google AI Studio](https://aistudio.google.com/apikey) |
| `PINECONE_API_KEY` | Yes | [Pinecone Console](https://app.pinecone.io) |
| `NEO4J_URI` | No | Only for opportunity banking |
| `NEXT_PUBLIC_AGENT_OS_URL` | Frontend only | Your backend Replit URL |

## License

MIT
