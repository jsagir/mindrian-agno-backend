"""
Larry Agents - All Roles

Each Larry role is a specialized Agno Agent with specific instructions
and access to PWS Brain tools for RAG-enhanced responses.

Features:
- Pinecone RAG for PWS course knowledge (325+ chunks)
- Neo4j for opportunity banking
- Reasoning/thinking visualization
- Tool call display
"""

import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.db.sqlite import AsyncSqliteDb
from agno.tools import tool

from prompts.larry_prompts import (
    LARRY_CLARIFIER_PROMPT,
    LARRY_COACH_PROMPT,
    LARRY_TEACHER_PROMPT,
    LARRY_PWS_INSTRUCTOR_PROMPT,
    LARRY_DEVIL_PROMPT,
    LARRY_SYNTHESIZER_PROMPT,
    LARRY_EXPERT_PROMPT,
)

# Import external tools (Tavily, Neo4j, Pinecone - direct API for Gemini)
from tools.external_tools import (
    TAVILY_TOOLS,
    NEO4J_TOOLS,
    PINECONE_TOOLS,
    ALL_EXTERNAL_TOOLS,
)


# =============================================================================
# PWS BRAIN TOOLS (Pinecone RAG)
# =============================================================================

def _search_pws_impl(query: str, top_k: int = 5) -> str:
    """Internal implementation for knowledge search using neo4j-knowledge-base."""
    try:
        from pinecone import Pinecone

        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            return "Knowledge base not available: PINECONE_API_KEY not set"

        pc = Pinecone(api_key=api_key)

        # Use neo4j-knowledge-base as primary (multilingual-e5-large embeddings)
        index_host = "https://neo4j-knowledge-base-bc1849d.svc.aped-4627-b74a.pinecone.io"
        index = pc.Index(host=index_host)

        # Search using Pinecone's integrated inference
        results = index.search(
            namespace="",
            query={
                "inputs": {"text": query},
                "top_k": top_k
            },
            include_metadata=True,
        )

        # Handle different response formats
        matches = []
        if hasattr(results, 'matches'):
            matches = results.matches
        elif isinstance(results, dict):
            matches = results.get("matches", [])

        if not matches:
            return f"No knowledge found for: {query}"

        output_parts = [f"## Knowledge: {query}\n"]
        output_parts.append("*Index: neo4j-knowledge-base | Model: multilingual-e5-large*\n")

        for i, match in enumerate(matches, 1):
            if hasattr(match, 'score'):
                score = match.score
                metadata = match.metadata or {}
            else:
                score = match.get("score", 0)
                metadata = match.get("metadata", {})

            title = metadata.get("title", metadata.get("name", "Untitled"))
            content = metadata.get("text", metadata.get("content", "No content"))
            source = metadata.get("source", metadata.get("type", "Knowledge Base"))

            output_parts.append(f"### {i}. {title}")
            output_parts.append(f"**Relevance:** {score:.2f}")
            output_parts.append(f"\n{content}\n")
            output_parts.append(f"*Source: {source}*\n---")

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error searching knowledge: {str(e)}"


@tool
def search_pws_knowledge(query: str, top_k: int = 5) -> str:
    """
    Search PWS course knowledge base for relevant content.

    Use this tool when you need to:
    - Find PWS framework information (JTBD, Minto, S-Curve, etc.)
    - Ground your advice in actual course methodology
    - Answer questions about innovation frameworks
    - Provide citations from PWS materials

    Args:
        query: The search query (e.g., "jobs to be done framework")
        top_k: Number of results to return (default 5)

    Returns:
        Formatted string with relevant PWS knowledge chunks
    """
    return _search_pws_impl(query, top_k)


@tool
def get_framework_details(framework_name: str) -> str:
    """
    Get detailed information about a specific PWS framework.

    Use this for detailed framework explanations:
    - JTBD / Jobs to Be Done
    - Minto Pyramid / SCQA
    - S-Curve Analysis
    - Four Lenses of Innovation
    - White Space Mapping
    - Scenario Analysis
    - PWS Validation Scorecard

    Args:
        framework_name: Name of the framework

    Returns:
        Detailed framework information from PWS course
    """
    framework_aliases = {
        "jtbd": "jobs to be done JTBD hire product progress milkshake",
        "jobs to be done": "jobs to be done JTBD milkshake hire progress",
        "minto": "minto pyramid SCQA situation complication question answer",
        "scqa": "SCQA situation complication question answer pyramid",
        "s-curve": "s-curve technology adoption lifecycle innovation",
        "four lenses": "four lenses innovation orthodoxies trends competencies",
        "white space": "white space mapping opportunity gap market",
        "scenario analysis": "scenario analysis 2x2 matrix future planning",
        "pws validation": "PWS validation scorecard GO NO-GO criteria",
    }

    search_term = framework_aliases.get(
        framework_name.lower(),
        f"{framework_name} framework methodology PWS innovation"
    )

    return _search_pws_impl(search_term, top_k=7)


# =============================================================================
# OPPORTUNITY BANKING TOOLS (Neo4j via MCP)
# =============================================================================

@tool
def save_opportunity(
    title: str,
    description: str,
    problem_statement: str,
    target_user: str,
    value_proposition: str,
    pws_score: int = 0,
    status: str = "draft"
) -> str:
    """
    Save an opportunity to the knowledge graph for later retrieval.

    Use this when:
    - User wants to bank/save an opportunity idea
    - A validated opportunity should be stored
    - User explicitly says "save this" or "bank this"

    Args:
        title: Short opportunity title
        description: Full description
        problem_statement: The clarified problem (SCQA format preferred)
        target_user: Who has this problem
        value_proposition: What value is delivered
        pws_score: PWS validation score (0-100)
        status: draft, validated, active, archived

    Returns:
        Confirmation with opportunity ID
    """
    import requests
    import json
    from datetime import datetime

    try:
        # Create opportunity node via Neo4j MCP
        opportunity_id = f"opp-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        cypher = """
        CREATE (o:Opportunity {
            id: $id,
            title: $title,
            description: $description,
            problem_statement: $problem_statement,
            target_user: $target_user,
            value_proposition: $value_proposition,
            pws_score: $pws_score,
            status: $status,
            created_at: datetime(),
            updated_at: datetime()
        })
        RETURN o.id as id, o.title as title
        """

        # Use neo4j driver directly since MCP is available in Claude
        from neo4j import GraphDatabase

        neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        neo4j_password = os.getenv("NEO4J_PASSWORD", "")

        driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        with driver.session() as session:
            result = session.run(cypher, {
                "id": opportunity_id,
                "title": title,
                "description": description,
                "problem_statement": problem_statement,
                "target_user": target_user,
                "value_proposition": value_proposition,
                "pws_score": pws_score,
                "status": status
            })
            record = result.single()
        driver.close()

        return f"✅ Opportunity saved!\n- **ID:** {opportunity_id}\n- **Title:** {title}\n- **Status:** {status}"

    except Exception as e:
        return f"Could not save opportunity: {str(e)}"


@tool
def list_opportunities(status: str = "all", limit: int = 10) -> str:
    """
    List saved opportunities from the knowledge graph.

    Use this when:
    - User wants to see their banked opportunities
    - User asks "what opportunities do I have?"
    - User wants to review past ideas

    Args:
        status: Filter by status (all, draft, validated, active, archived)
        limit: Max number to return

    Returns:
        Formatted list of opportunities
    """
    try:
        from neo4j import GraphDatabase

        neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        neo4j_password = os.getenv("NEO4J_PASSWORD", "")

        cypher = """
        MATCH (o:Opportunity)
        WHERE $status = 'all' OR o.status = $status
        RETURN o.id as id, o.title as title, o.status as status,
               o.pws_score as score, o.target_user as target
        ORDER BY o.created_at DESC
        LIMIT $limit
        """

        driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        with driver.session() as session:
            result = session.run(cypher, {"status": status, "limit": limit})
            records = list(result)
        driver.close()

        if not records:
            return "No opportunities found. Start exploring and save promising ideas!"

        output = ["## 📋 Your Opportunities\n"]
        for rec in records:
            score_display = f"PWS: {rec['score']}/100" if rec['score'] else "Not scored"
            output.append(
                f"- **{rec['title']}** ({rec['status']})\n"
                f"  - ID: `{rec['id']}`\n"
                f"  - Target: {rec['target']}\n"
                f"  - {score_display}"
            )

        return "\n".join(output)

    except Exception as e:
        return f"Could not list opportunities: {str(e)}"


@tool
def get_opportunity(opportunity_id: str) -> str:
    """
    Get full details of a specific opportunity.

    Args:
        opportunity_id: The opportunity ID to retrieve

    Returns:
        Full opportunity details
    """
    try:
        from neo4j import GraphDatabase

        neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        neo4j_password = os.getenv("NEO4J_PASSWORD", "")

        cypher = """
        MATCH (o:Opportunity {id: $id})
        RETURN o
        """

        driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        with driver.session() as session:
            result = session.run(cypher, {"id": opportunity_id})
            record = result.single()
        driver.close()

        if not record:
            return f"Opportunity not found: {opportunity_id}"

        o = record["o"]
        return f"""## 📌 {o['title']}

**Status:** {o['status']} | **PWS Score:** {o.get('pws_score', 'N/A')}/100

### Problem Statement
{o['problem_statement']}

### Target User
{o['target_user']}

### Value Proposition
{o['value_proposition']}

### Description
{o['description']}

---
*ID: {o['id']}*
"""

    except Exception as e:
        return f"Could not retrieve opportunity: {str(e)}"


# =============================================================================
# SHARED AGENT CONFIGURATION
# =============================================================================

# Model configuration - Gemini 3 as primary
def get_gemini_model():
    """Get Gemini 3 model with API key."""
    return Gemini(
        id="gemini-3-flash-preview",
        api_key=os.getenv("GOOGLE_AI_API_KEY"),
    )


# Shared tools for all agents
PWS_TOOLS = [search_pws_knowledge, get_framework_details]
OPPORTUNITY_TOOLS = [save_opportunity, list_opportunities, get_opportunity]

# Combine all tools (including external services for Gemini)
ALL_TOOLS = PWS_TOOLS + OPPORTUNITY_TOOLS + ALL_EXTERNAL_TOOLS


# =============================================================================
# PINECONE KNOWLEDGE BASE (RAG)
# =============================================================================

# NOTE: PWS Knowledge base uses Pinecone's integrated inference via the search_pws_knowledge tool.
# The pws-world index has 1024 dimensions from text-embedding-3-large.
# Agents use the search_pws_knowledge tool for RAG instead of automatic knowledge injection.
pws_knowledge = None  # Disabled - use search_pws_knowledge tool instead


# =============================================================================
# LARRY AGENTS
# =============================================================================

# Shared database for all agents
mindrian_db = AsyncSqliteDb(db_file="mindrian.db", session_table="agent_sessions")

# Larry the Clarifier (Default)
larry_clarifier = Agent(
    name="Larry the Clarifier",
    id="larry-clarifier",
    model=get_gemini_model(),
    instructions=[LARRY_CLARIFIER_PROMPT],
    tools=ALL_TOOLS,
    markdown=True,
    db=mindrian_db,
    knowledge=pws_knowledge,  # Pinecone RAG for PWS content
    search_knowledge=True,  # Auto-search knowledge base
    add_knowledge_to_context=True,  # Add retrieved knowledge to context
    description="Asks questions to understand your challenge (max 5, then provides value)",
    reasoning=True,  # Enable thinking/reasoning display
    stream_intermediate_steps=True,  # Stream tool calls and reasoning
)

# Larry the Coach
larry_coach = Agent(
    name="Larry the Coach",
    id="larry-coach",
    model=get_gemini_model(),
    instructions=[LARRY_COACH_PROMPT],
    tools=ALL_TOOLS,
    markdown=True,
    db=mindrian_db,
    knowledge=pws_knowledge,
    search_knowledge=True,
    add_knowledge_to_context=True,
    description="Step-by-step guidance through PWS frameworks",
    reasoning=True,
    stream_intermediate_steps=True,
)

# Larry the Teacher - RAG-first, conversational, no reasoning
larry_teacher = Agent(
    name="Larry the Teacher",
    id="larry-teacher",
    model=get_gemini_model(),
    instructions=[LARRY_TEACHER_PROMPT],
    tools=ALL_TOOLS,
    markdown=True,
    db=mindrian_db,
    knowledge=pws_knowledge,
    search_knowledge=True,
    add_knowledge_to_context=True,
    description="Deep-dive education on innovation frameworks",
    reasoning=False,  # No reasoning - RAG-first conversational mode
    stream_intermediate_steps=True,
)

# Larry the PWS Instructor - RAG-first, conversational, no reasoning
larry_pws_instructor = Agent(
    name="Larry the PWS Instructor",
    id="larry-pws-instructor",
    model=get_gemini_model(),
    instructions=[LARRY_PWS_INSTRUCTOR_PROMPT],
    tools=ALL_TOOLS,
    markdown=True,
    db=mindrian_db,
    knowledge=pws_knowledge,
    search_knowledge=True,
    add_knowledge_to_context=True,
    description="Hands-on PWS methodology implementation",
    reasoning=False,  # No reasoning - RAG-first conversational mode
    stream_intermediate_steps=True,
)

# Larry the Devil's Advocate
larry_devil = Agent(
    name="Larry the Devil's Advocate",
    id="larry-devil",
    model=get_gemini_model(),
    instructions=[LARRY_DEVIL_PROMPT],
    tools=ALL_TOOLS,
    markdown=True,
    db=mindrian_db,
    knowledge=pws_knowledge,
    search_knowledge=True,
    add_knowledge_to_context=True,
    description="Challenge assumptions and stress-test ideas",
    reasoning=True,
    stream_intermediate_steps=True,
)

# Larry the Synthesizer
larry_synthesizer = Agent(
    name="Larry the Synthesizer",
    id="larry-synthesizer",
    model=get_gemini_model(),
    instructions=[LARRY_SYNTHESIZER_PROMPT],
    tools=ALL_TOOLS,
    markdown=True,
    db=mindrian_db,
    knowledge=pws_knowledge,
    search_knowledge=True,
    add_knowledge_to_context=True,
    description="Organize discussion into structured insights",
    reasoning=True,
    stream_intermediate_steps=True,
)

# Larry the Expert
larry_expert = Agent(
    name="Larry the Expert",
    id="larry-expert",
    model=get_gemini_model(),
    instructions=[LARRY_EXPERT_PROMPT],
    tools=ALL_TOOLS,
    markdown=True,
    db=mindrian_db,
    knowledge=pws_knowledge,
    search_knowledge=True,
    add_knowledge_to_context=True,
    description="Domain expertise and methodology application",
    reasoning=True,
    stream_intermediate_steps=True,
)


# =============================================================================
# AGENT REGISTRY
# =============================================================================

LARRY_AGENTS = {
    "clarifier": larry_clarifier,
    "coach": larry_coach,
    "teacher": larry_teacher,
    "pws_instructor": larry_pws_instructor,
    "devil": larry_devil,
    "synthesizer": larry_synthesizer,
    "expert": larry_expert,
}


def get_agent(role: str) -> Agent:
    """Get an agent by role name."""
    return LARRY_AGENTS.get(role, larry_clarifier)


def list_agents() -> list[dict]:
    """List all available agents with metadata."""
    from prompts.larry_prompts import ROLE_METADATA

    return [
        {
            "id": role_id,
            "name": meta["name"],
            "icon": meta["icon"],
            "description": meta["description"],
        }
        for role_id, meta in ROLE_METADATA.items()
    ]
