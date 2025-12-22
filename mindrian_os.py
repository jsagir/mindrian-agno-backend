"""
Mindrian AgentOS - Main Application

This is the main entry point for the Mindrian AgentOS.
It runs on port 7777 and connects to Agno Agent UI.

Features:
- 7 Larry roles (Clarifier, Coach, Teacher, PWS Instructor, Devil, Synthesizer, Expert)
- 4 Specialist agents (Minto Analyst, RS Hunter, Data Extractor, Master Strategist)
- PWS Brain integration (Pinecone RAG with 1,371 course records)
- FastMCP Cloud tools (Minto, Reverse Salients, LangExtract)
- Team coordination (5 teams)
- Session persistence (SQLite)
"""

import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from agno.os import AgentOS

# Import all agents
from agents.larry import (
    larry_clarifier,
    larry_coach,
    larry_teacher,
    larry_pws_instructor,
    larry_devil,
    larry_synthesizer,
    larry_expert,
)

# Import specialist agents
from agents.specialists import (
    minto_analyst,
    reverse_salient_hunter,
    data_extractor,
    master_strategist,
)

# Import teams
from teams.clarification import clarification_team
from teams.analysis import analysis_team
from teams.validation import validation_team
from teams.exploration import exploration_team
from teams.discovery import discovery_team


# =============================================================================
# AGENT OS CONFIGURATION
# =============================================================================

# Create AgentOS with all agents
mindrian_os = AgentOS(
    id="mindrian",
    description="Mindrian Innovation Platform - AI-Powered Thinking Partner",
    agents=[
        # Larry agents (conversational roles)
        larry_clarifier,
        larry_coach,
        larry_teacher,
        larry_pws_instructor,
        larry_devil,
        larry_synthesizer,
        larry_expert,
        # Specialist agents (advanced tools)
        minto_analyst,
        reverse_salient_hunter,
        data_extractor,
        master_strategist,
    ],
    teams=[
        clarification_team,
        analysis_team,
        validation_team,
        exploration_team,
        discovery_team,
    ],
)

# Get the FastAPI app
app = mindrian_os.get_app()


# =============================================================================
# CUSTOM ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "Mindrian AgentOS",
        "version": "2.0.0",
        "description": "AI-Powered Innovation Platform with FastMCP Cloud Tools",
        "agents": {
            "larry": [
                {"id": "larry-clarifier", "name": "Larry the Clarifier", "icon": "search"},
                {"id": "larry-coach", "name": "Larry the Coach", "icon": "compass"},
                {"id": "larry-teacher", "name": "Larry the Teacher", "icon": "graduation-cap"},
                {"id": "larry-pws-instructor", "name": "Larry the PWS Instructor", "icon": "target"},
                {"id": "larry-devil", "name": "Larry the Devil's Advocate", "icon": "swords"},
                {"id": "larry-synthesizer", "name": "Larry the Synthesizer", "icon": "layers"},
                {"id": "larry-expert", "name": "Larry the Expert", "icon": "brain"},
            ],
            "specialists": [
                {"id": "minto-analyst", "name": "Minto Analyst", "icon": "pyramid", "description": "SCQA/MECE pyramid analysis"},
                {"id": "rs-hunter", "name": "Reverse Salient Hunter", "icon": "target", "description": "Innovation opportunity discovery"},
                {"id": "data-extractor", "name": "Data Extractor", "icon": "database", "description": "Structured data extraction"},
                {"id": "master-strategist", "name": "Master Strategist", "icon": "brain", "description": "Comprehensive strategic analysis"},
            ],
        },
        "teams": [
            {"id": "clarification-team", "name": "Clarification Team", "description": "Clarify problems through questioning and challenge"},
            {"id": "analysis-team", "name": "Analysis Team", "description": "Apply PWS frameworks for deep analysis"},
            {"id": "validation-team", "name": "Validation Team", "description": "Validate opportunities with PWS scorecard"},
            {"id": "exploration-team", "name": "Exploration Team", "description": "Explore future possibilities"},
            {"id": "discovery-team", "name": "Discovery Team", "description": "Advanced innovation discovery with Minto + RS"},
        ],
        "tools": {
            "pws_brain": ["search_pws_knowledge", "get_framework_details"],
            "minto": ["plan_pyramid", "develop_scqa_framework", "generate_mece_framework", "run_complete_minto_analysis"],
            "reverse_salients": ["initialize_discovery", "find_reverse_salients", "validate_reverse_salient", "execute_full_rs_workflow"],
            "extraction": ["extract_structured_data", "extract_from_url"],
        },
        "docs": "/docs",
        "agent_ui": "http://localhost:3000",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    # Check API keys
    google_ok = bool(os.getenv("GOOGLE_AI_API_KEY"))
    pinecone_ok = bool(os.getenv("PINECONE_API_KEY"))
    neo4j_ok = bool(os.getenv("NEO4J_URI"))

    all_ok = google_ok and pinecone_ok

    return {
        "status": "healthy" if all_ok else "degraded",
        "services": {
            "google_ai": "connected" if google_ok else "missing_api_key",
            "pinecone": "connected" if pinecone_ok else "missing_api_key",
            "neo4j": "connected" if neo4j_ok else "missing_uri",
        },
        "fastmcp_servers": {
            "pyramidlogicmintomindrian": "https://pyramidlogicmintomindrian.fastmcp.app",
            "mindrianmcp-minto": "https://mindrianmcp-minto.fastmcp.app",
            "extracormcp-mindrian": "https://extracormcp-mindrian.fastmcp.app",
            "mindrianrs-mcp": "https://mindrianrs-mcp.fastmcp.app",
        },
    }


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("MINDRIAN AGENT OS v2.0")
    print("=" * 60)
    print()
    print("Starting Mindrian AgentOS on http://localhost:7777")
    print()
    print("Larry Agents (Conversational Roles):")
    print("  - Larry the Clarifier (default)")
    print("  - Larry the Coach")
    print("  - Larry the Teacher")
    print("  - Larry the PWS Instructor")
    print("  - Larry the Devil's Advocate")
    print("  - Larry the Synthesizer")
    print("  - Larry the Expert")
    print()
    print("Specialist Agents (Advanced Tools):")
    print("  - Minto Analyst (SCQA/MECE analysis)")
    print("  - Reverse Salient Hunter (innovation discovery)")
    print("  - Data Extractor (structured extraction)")
    print("  - Master Strategist (comprehensive analysis)")
    print()
    print("Teams:")
    print("  - Clarification Team (Clarifier + Devil + Synthesizer)")
    print("  - Analysis Team (PWS Instructor + Expert + Coach)")
    print("  - Validation Team (PWS Instructor + Devil + Expert)")
    print("  - Exploration Team (Clarifier + Teacher + Synthesizer)")
    print("  - Discovery Team (Minto + RS Hunter + Strategist)")
    print()
    print("FastMCP Cloud Tools:")
    print("  - Minto Pyramid (pyramidlogicmintomindrian.fastmcp.app)")
    print("  - SCQA Framework (mindrianmcp-minto.fastmcp.app)")
    print("  - LangExtract (extracormcp-mindrian.fastmcp.app)")
    print("  - Reverse Salients (mindrianrs-mcp.fastmcp.app)")
    print()
    print("Connect Agent UI at: http://localhost:3000")
    print("API Docs at: http://localhost:7777/docs")
    print("=" * 60)
    print()

    # Check for required API keys
    if not os.getenv("GOOGLE_AI_API_KEY"):
        print("WARNING: GOOGLE_AI_API_KEY not set. Agent responses will fail.")
    if not os.getenv("PINECONE_API_KEY"):
        print("WARNING: PINECONE_API_KEY not set. PWS Brain search will fail.")
    if not os.getenv("NEO4J_URI"):
        print("INFO: NEO4J_URI not set. Opportunity banking disabled.")

    # Start the server
    import uvicorn
    port = int(os.getenv("PORT", 7777))
    uvicorn.run(app, host="0.0.0.0", port=port)
