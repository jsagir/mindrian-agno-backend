"""
FastMCP Cloud Tools - Migrated from Windows Claude Desktop

These tools connect to FastMCP cloud deployments for advanced Mindrian capabilities:
1. Pyramid Logic / Minto Analysis
2. SCQA + MECE Framework
3. LangExtract Data Extraction
4. Reverse Salient Discovery

Each tool wraps a FastMCP endpoint for use in Agno agents.
"""

import os
import httpx
from agno.tools import tool
from typing import Optional


# =============================================================================
# FASTMCP CLIENT HELPER
# =============================================================================

def call_fastmcp_tool(server_url: str, tool_name: str, arguments: dict) -> dict:
    """Call a FastMCP cloud tool via MCP-over-HTTP."""
    try:
        response = httpx.post(
            f"{server_url}/tools/{tool_name}",
            json={"arguments": arguments},
            timeout=120.0,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


# =============================================================================
# PYRAMID LOGIC / MINTO TOOLS (pyramidlogicmintomindrian)
# =============================================================================

PYRAMID_SERVER = "https://pyramidlogicmintomindrian.fastmcp.app"


@tool
def plan_pyramid(question: str, context: str = "") -> str:
    """
    Plan a complete Pyramid/Minto analysis (Stage 1).

    Returns ReasoningPlan with governing thoughts, MECE reasons, and evidence tasks.

    Args:
        question: The question or problem to analyze
        context: Additional context for the analysis

    Returns:
        ReasoningPlan with stages outlined
    """
    result = call_fastmcp_tool(PYRAMID_SERVER, "plan_pyramid", {
        "question": question,
        "context": context
    })
    return str(result)


@tool
def run_pyramid_stage(plan_id: str, stage: int) -> str:
    """
    Execute evidence gathering for a Pyramid stage (Stage 2).

    Calls Tavily search and collects evidence with citations.

    Args:
        plan_id: The plan ID from plan_pyramid
        stage: Stage number to execute (1-5)

    Returns:
        Evidence gathered for the stage
    """
    result = call_fastmcp_tool(PYRAMID_SERVER, "run_plan_stage", {
        "plan_id": plan_id,
        "stage": stage
    })
    return str(result)


@tool
def synthesize_pyramid_analysis(plan_id: str) -> str:
    """
    Synthesize final Pyramid/Minto deliverable (Stage 3).

    Performs quality checks and generates structured output with citations.

    Args:
        plan_id: The plan ID from plan_pyramid

    Returns:
        Synthesized Pyramid analysis
    """
    result = call_fastmcp_tool(PYRAMID_SERVER, "synthesize_pyramid", {
        "plan_id": plan_id
    })
    return str(result)


@tool
def critique_pyramid(plan_id: str) -> str:
    """
    Run systematic critique against Pyramid/Minto rubric (Stage 4).

    Evaluates fidelity, evidence sufficiency, and consistency.

    Args:
        plan_id: The plan ID to critique

    Returns:
        Critique results with improvement suggestions
    """
    result = call_fastmcp_tool(PYRAMID_SERVER, "critique_pyramid_tool", {
        "plan_id": plan_id
    })
    return str(result)


@tool
def finalize_pyramid(plan_id: str, format: str = "markdown") -> str:
    """
    Finalize and export the Pyramid analysis (Stage 5).

    Args:
        plan_id: The plan ID to finalize
        format: Output format (markdown, json, html)

    Returns:
        Final deliverable
    """
    result = call_fastmcp_tool(PYRAMID_SERVER, "finalize_pyramid", {
        "plan_id": plan_id,
        "format": format
    })
    return str(result)


# =============================================================================
# MINTO SCQA FRAMEWORK TOOLS (mindrianmcp-minto)
# =============================================================================

MINTO_SERVER = "https://mindrianmcp-minto.fastmcp.app"


@tool
def initialize_minto_analysis(input_text: str, analysis_goal: str, session_id: str = "") -> str:
    """
    Initialize a new Minto pyramid analysis session.

    Args:
        input_text: The text or problem to analyze
        analysis_goal: What the analysis aims to achieve
        session_id: Optional session ID (auto-generated if not provided)

    Returns:
        Session information and initial analysis plan
    """
    result = call_fastmcp_tool(MINTO_SERVER, "initialize_minto_analysis", {
        "input_text": input_text,
        "analysis_goal": analysis_goal,
        "session_id": session_id
    })
    return str(result)


@tool
def develop_scqa_framework(session_id: str, situation_context: str = "", complication_hint: str = "") -> str:
    """
    Develop complete SCQA framework using sequential thinking.

    Creates:
    - Situation: Current state and importance
    - Complication: The paradox or fundamental tension
    - Question: Opportunity-revealing question
    - [NO ANSWER]: Reveals, doesn't prescribe

    Args:
        session_id: The analysis session ID
        situation_context: Optional hints about the situation
        complication_hint: Optional hints about the complication

    Returns:
        Complete SCQA framework with thinking steps
    """
    result = call_fastmcp_tool(MINTO_SERVER, "develop_scqa_framework", {
        "session_id": session_id,
        "situation_context": situation_context,
        "complication_hint": complication_hint
    })
    return str(result)


@tool
def generate_mece_framework(session_id: str, max_iterations: int = 3) -> str:
    """
    Generate MECE framework with iterative refinement.

    Implements revision pattern:
    1. Propose initial framework
    2. Validate MECE properties
    3. If weak, revise and retry
    4. Continue until validation passes

    Args:
        session_id: The analysis session ID
        max_iterations: Maximum attempts (default 3)

    Returns:
        Validated MECE framework with revision history
    """
    result = call_fastmcp_tool(MINTO_SERVER, "generate_mece_framework", {
        "session_id": session_id,
        "max_iterations": max_iterations
    })
    return str(result)


@tool
def gather_minto_evidence(session_id: str, max_results: int = 10) -> str:
    """
    Gather evidence for each MECE category using web search.

    Features:
    - Query optimization for each category
    - Advanced search mode for quality
    - Recency filters (2024-2025)
    - Citation extraction

    Args:
        session_id: The analysis session ID
        max_results: Results per search (default 10)

    Returns:
        Evidence organized by MECE category with citations
    """
    result = call_fastmcp_tool(MINTO_SERVER, "gather_evidence", {
        "session_id": session_id,
        "max_results_per_query": max_results
    })
    return str(result)


@tool
def run_complete_minto_analysis(input_text: str, analysis_goal: str, include_meta: bool = True) -> str:
    """
    Run complete Minto pyramid analysis in one call.

    Orchestrates all 6 phases:
    1. Initialize session
    2. Develop SCQA framework
    3. Generate MECE framework (with iterations)
    4. Gather evidence
    5. Synthesize pyramid
    6. Perform meta-analysis

    Args:
        input_text: The problem/situation to analyze
        analysis_goal: What the analysis should achieve
        include_meta: Whether to include Phase 6 meta-analysis

    Returns:
        Complete Minto pyramid with full process documentation
    """
    result = call_fastmcp_tool(MINTO_SERVER, "run_complete_minto_analysis", {
        "input_text": input_text,
        "analysis_goal": analysis_goal,
        "include_meta_analysis": include_meta
    })
    return str(result)


# =============================================================================
# LANGEXTRACT DATA EXTRACTION TOOLS (extracormcp-mindrian)
# =============================================================================

EXTRACTOR_SERVER = "https://extracormcp-mindrian.fastmcp.app"


@tool
def extract_structured_data(
    text: str,
    prompt_description: str,
    examples: list = None,
    extraction_passes: int = 2,
    max_workers: int = 10
) -> str:
    """
    Extract structured information from text using LangExtract.

    Args:
        text: The input text to extract from
        prompt_description: Clear instructions for what to extract
        examples: List of example extractions (few-shot learning)
        extraction_passes: Number of passes (1-5, more = higher recall)
        max_workers: Parallel workers (1-50, more = faster)

    Returns:
        Structured extractions in JSON format

    Example:
        extract_structured_data(
            text="Dr. Smith prescribed 50mg aspirin.",
            prompt_description="Extract medications with dosage",
            examples=[{
                "text": "Take 100mg ibuprofen",
                "extractions": [{"class": "medication", "text": "ibuprofen", "dosage": "100mg"}]
            }]
        )
    """
    result = call_fastmcp_tool(EXTRACTOR_SERVER, "extract_structured_data", {
        "text": text,
        "prompt_description": prompt_description,
        "examples": examples or [],
        "extraction_passes": extraction_passes,
        "max_workers": max_workers
    })
    return str(result)


@tool
def extract_from_url(
    url: str,
    prompt_description: str,
    examples: list = None,
    extraction_passes: int = 2
) -> str:
    """
    Extract structured information directly from a URL.

    Args:
        url: URL to fetch and extract from
        prompt_description: Extraction instructions
        examples: Few-shot examples
        extraction_passes: Number of passes (default 2 for URLs)

    Returns:
        Structured extractions from URL content
    """
    result = call_fastmcp_tool(EXTRACTOR_SERVER, "extract_from_url", {
        "url": url,
        "prompt_description": prompt_description,
        "examples": examples or [],
        "extraction_passes": extraction_passes
    })
    return str(result)


# =============================================================================
# REVERSE SALIENT DISCOVERY TOOLS (mindrianrs-mcp)
# =============================================================================

RS_SERVER = "https://mindrianrs-mcp.fastmcp.app"


@tool
def initialize_discovery(challenge: str, domains: list, constraints: list = None) -> str:
    """
    Initialize Mindrian Reverse Salient Discovery session.

    Reverse Salients are innovation opportunities found at the intersection
    of domains that share methods but not meaning.

    Args:
        challenge: Description of the innovation challenge
        domains: List of domains to explore, each with:
            - label: Domain name
            - concepts: Key concepts
            - methods: Key methods
            - problems: Key problems
        constraints: List of constraints

    Returns:
        Session information and analysis plan

    Example:
        initialize_discovery(
            challenge="Find innovation opportunities in healthcare AI",
            domains=[
                {"label": "Medical Imaging", "concepts": ["radiology", "CT"], "methods": ["CNN", "segmentation"]},
                {"label": "Drug Discovery", "concepts": ["molecules", "proteins"], "methods": ["GNN", "simulation"]}
            ]
        )
    """
    result = call_fastmcp_tool(RS_SERVER, "initialize_discovery", {
        "structured_input": {
            "challenge": challenge,
            "domains": domains,
            "constraints": constraints or []
        }
    })
    return str(result)


@tool
def collect_papers_tavily(session_id: str, search_queries: list, max_results: int = 10) -> str:
    """
    Collect papers using Tavily web search.

    Args:
        session_id: Discovery session ID
        search_queries: List of search queries
        max_results: Maximum results per query

    Returns:
        Collection results with thinking summary
    """
    result = call_fastmcp_tool(RS_SERVER, "collect_papers_tavily", {
        "session_id": session_id,
        "search_queries": search_queries,
        "max_results_per_query": max_results
    })
    return str(result)


@tool
def compute_lsa_similarity(session_id: str, n_components: int = 100) -> str:
    """
    Compute STRUCTURAL similarity using LSA (TF-IDF + SVD).

    Measures shared methods, techniques, and terminology between papers.
    High LSA = papers use similar vocabulary/methods.

    Args:
        session_id: Discovery session ID
        n_components: Number of SVD components (topics)

    Returns:
        LSA similarity matrix with thinking summary
    """
    result = call_fastmcp_tool(RS_SERVER, "compute_lsa_similarity", {
        "session_id": session_id,
        "n_components": n_components
    })
    return str(result)


@tool
def compute_bert_similarity(session_id: str, bert_model: str = "all-MiniLM-L6-v2") -> str:
    """
    Compute SEMANTIC similarity using BERT embeddings.

    Measures shared meaning, context, and application domains.
    High BERT = papers discuss similar concepts/applications.

    Args:
        session_id: Discovery session ID
        bert_model: BERT model to use

    Returns:
        BERT similarity matrix with thinking summary
    """
    result = call_fastmcp_tool(RS_SERVER, "compute_bert_similarity", {
        "session_id": session_id,
        "bert_model": bert_model
    })
    return str(result)


@tool
def find_reverse_salients(session_id: str, top_n: int = 10) -> str:
    """
    Find reverse salients through differential analysis.

    THE KEY INSIGHT: High LSA + Low BERT = Innovation Opportunity!

    Papers that share methods but NOT meaning indicate:
    - Techniques that could transfer across domains
    - Unexplored applications of proven methods
    - Gaps in the knowledge network

    Args:
        session_id: Discovery session ID
        top_n: Number of top opportunities to return

    Returns:
        Reverse salients ranked by innovation potential
    """
    result = call_fastmcp_tool(RS_SERVER, "find_reverse_salients", {
        "session_id": session_id,
        "top_n": top_n
    })
    return str(result)


@tool
def validate_reverse_salient(
    session_id: str,
    reverse_salient_id: str,
    check_patents: bool = True,
    check_startups: bool = True,
    check_citations: bool = True
) -> str:
    """
    Advanced validation of a reverse salient opportunity.

    Checks:
    - Patent activity (is it already protected?)
    - Startup activity (is anyone working on it?)
    - Citation networks (how connected are the papers?)

    Args:
        session_id: Discovery session ID
        reverse_salient_id: RS ID to validate (e.g., "RS-001")
        check_patents: Search patent databases
        check_startups: Search startup activity
        check_citations: Analyze citation networks

    Returns:
        Validation results with novelty score
    """
    result = call_fastmcp_tool(RS_SERVER, "validate_reverse_salient", {
        "session_id": session_id,
        "reverse_salient_id": reverse_salient_id,
        "check_patents": check_patents,
        "check_startups": check_startups,
        "check_citations": check_citations
    })
    return str(result)


@tool
def develop_innovation_thesis(session_id: str, reverse_salient_id: str) -> str:
    """
    Develop complete innovation thesis for a reverse salient.

    Creates a structured opportunity report with:
    - Problem statement (SCQA format)
    - Market opportunity
    - Technical feasibility
    - Competitive landscape
    - Recommended next steps

    Args:
        session_id: Discovery session ID
        reverse_salient_id: RS ID (e.g., "RS-001")

    Returns:
        Complete innovation opportunity report
    """
    result = call_fastmcp_tool(RS_SERVER, "develop_innovation_thesis", {
        "session_id": session_id,
        "reverse_salient_id": reverse_salient_id
    })
    return str(result)


@tool
def execute_full_rs_workflow(
    challenge: str,
    domains: list,
    search_queries: list,
    validate_top_n: int = 3
) -> str:
    """
    Execute complete Mindrian Reverse Salient discovery workflow.

    Full pipeline:
    1. Initialize discovery session
    2. Collect papers via Tavily
    3. Clean and preprocess
    4. Compute LSA similarity (structural)
    5. Compute BERT similarity (semantic)
    6. Find reverse salients (High LSA + Low BERT)
    7. Validate top opportunities
    8. Generate final report

    Args:
        challenge: Innovation challenge description
        domains: List of domains to explore
        search_queries: Tavily search queries
        validate_top_n: Number of top RSs to validate

    Returns:
        Complete workflow results with ranked opportunities
    """
    result = call_fastmcp_tool(RS_SERVER, "execute_full_workflow", {
        "structured_input": {
            "challenge": challenge,
            "domains": domains
        },
        "search_queries": search_queries,
        "validate_top_n": validate_top_n
    })
    return str(result)


# =============================================================================
# TOOL COLLECTIONS
# =============================================================================

PYRAMID_TOOLS = [
    plan_pyramid,
    run_pyramid_stage,
    synthesize_pyramid_analysis,
    critique_pyramid,
    finalize_pyramid,
]

MINTO_TOOLS = [
    initialize_minto_analysis,
    develop_scqa_framework,
    generate_mece_framework,
    gather_minto_evidence,
    run_complete_minto_analysis,
]

EXTRACTOR_TOOLS = [
    extract_structured_data,
    extract_from_url,
]

REVERSE_SALIENT_TOOLS = [
    initialize_discovery,
    collect_papers_tavily,
    compute_lsa_similarity,
    compute_bert_similarity,
    find_reverse_salients,
    validate_reverse_salient,
    develop_innovation_thesis,
    execute_full_rs_workflow,
]

ALL_FASTMCP_TOOLS = PYRAMID_TOOLS + MINTO_TOOLS + EXTRACTOR_TOOLS + REVERSE_SALIENT_TOOLS
