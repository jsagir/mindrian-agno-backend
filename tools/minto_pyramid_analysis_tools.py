"""
Minto Pyramid Analysis Tools

Auto-generated from skill package: minto-pyramid-analysis
Version: 1.0.0
"""

import os
import httpx
from agno.tools import tool
from typing import Any, Optional


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def call_fastmcp_tool(server_url: str, tool_name: str, arguments: dict) -> dict:
    """Call a FastMCP cloud tool via HTTP."""
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
# TOOLS
# =============================================================================

@tool
def initialize_minto_analysis(input_text: str, analysis_goal: str, session_id: str = "None") -> str:
    """
    Initialize a new Minto pyramid analysis session
    """
    result = call_fastmcp_tool(
        "https://mindrianmcp-minto.fastmcp.app",
        "initialize_minto_analysis",
        {"input_text": input_text, "analysis_goal": analysis_goal, "session_id": session_id}
    )
    return str(result)


@tool
def develop_scqa_framework(session_id: str, situation_context: str = "None", complication_hint: str = "None") -> str:
    """
    Develop complete SCQA framework using sequential thinking
    """
    result = call_fastmcp_tool(
        "https://mindrianmcp-minto.fastmcp.app",
        "develop_scqa_framework",
        {"session_id": session_id, "situation_context": situation_context, "complication_hint": complication_hint}
    )
    return str(result)


@tool
def generate_mece_framework(session_id: str, max_iterations: int = 3) -> str:
    """
    Generate MECE framework with iterative validation
    """
    result = call_fastmcp_tool(
        "https://mindrianmcp-minto.fastmcp.app",
        "generate_mece_framework",
        {"session_id": session_id, "max_iterations": max_iterations}
    )
    return str(result)


@tool
def gather_minto_evidence(session_id: str, max_results_per_query: int = 10) -> str:
    """
    Gather evidence for each MECE category using web search
    """
    result = call_fastmcp_tool(
        "https://mindrianmcp-minto.fastmcp.app",
        "gather_evidence",
        {"session_id": session_id, "max_results_per_query": max_results_per_query}
    )
    return str(result)


@tool
def synthesize_pyramid(session_id: str, output_format: str = "markdown") -> str:
    """
    Synthesize complete Minto pyramid with evidence integration
    """
    result = call_fastmcp_tool(
        "https://mindrianmcp-minto.fastmcp.app",
        "synthesize_pyramid",
        {"session_id": session_id, "output_format": output_format}
    )
    return str(result)


@tool
def critique_pyramid(plan_id: str) -> str:
    """
    Run systematic critique against Minto rubric
    """
    result = call_fastmcp_tool(
        "https://pyramidlogicmintomindrian.fastmcp.app",
        "critique_pyramid_tool",
        {"plan_id": plan_id}
    )
    return str(result)


@tool
def finalize_pyramid(plan_id: str, format: str = "None") -> str:
    """
    Finalize and export the pyramid analysis
    """
    result = call_fastmcp_tool(
        "https://pyramidlogicmintomindrian.fastmcp.app",
        "finalize_pyramid",
        {"plan_id": plan_id, "format": format}
    )
    return str(result)


# =============================================================================
# EXPORTS
# =============================================================================

MINTO_PYRAMID_ANALYSIS_TOOLS = [initialize_minto_analysis, develop_scqa_framework, generate_mece_framework, gather_minto_evidence, synthesize_pyramid, critique_pyramid, finalize_pyramid]
