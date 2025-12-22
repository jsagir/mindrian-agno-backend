"""
Mindrian Tools Package

All Agno tools for the Mindrian platform.

Includes:
- PWS Brain Tools: Pinecone RAG for PWS course knowledge
- FastMCP Tools: Cloud-based advanced analysis (Minto, RS, Extraction)
"""

from tools.pws_brain import search_pws_knowledge, get_framework_details

from tools.fastmcp_tools import (
    # Pyramid Tools
    plan_pyramid,
    run_pyramid_stage,
    synthesize_pyramid_analysis,
    critique_pyramid,
    finalize_pyramid,
    PYRAMID_TOOLS,
    # Minto Tools
    initialize_minto_analysis,
    develop_scqa_framework,
    generate_mece_framework,
    gather_minto_evidence,
    run_complete_minto_analysis,
    MINTO_TOOLS,
    # Extractor Tools
    extract_structured_data,
    extract_from_url,
    EXTRACTOR_TOOLS,
    # Reverse Salient Tools
    initialize_discovery,
    collect_papers_tavily,
    compute_lsa_similarity,
    compute_bert_similarity,
    find_reverse_salients,
    validate_reverse_salient,
    develop_innovation_thesis,
    execute_full_rs_workflow,
    REVERSE_SALIENT_TOOLS,
    # All
    ALL_FASTMCP_TOOLS,
)

__all__ = [
    # PWS Brain
    "search_pws_knowledge",
    "get_framework_details",
    # Pyramid
    "plan_pyramid",
    "run_pyramid_stage",
    "synthesize_pyramid_analysis",
    "critique_pyramid",
    "finalize_pyramid",
    "PYRAMID_TOOLS",
    # Minto
    "initialize_minto_analysis",
    "develop_scqa_framework",
    "generate_mece_framework",
    "gather_minto_evidence",
    "run_complete_minto_analysis",
    "MINTO_TOOLS",
    # Extractor
    "extract_structured_data",
    "extract_from_url",
    "EXTRACTOR_TOOLS",
    # Reverse Salient
    "initialize_discovery",
    "collect_papers_tavily",
    "compute_lsa_similarity",
    "compute_bert_similarity",
    "find_reverse_salients",
    "validate_reverse_salient",
    "develop_innovation_thesis",
    "execute_full_rs_workflow",
    "REVERSE_SALIENT_TOOLS",
    # All
    "ALL_FASTMCP_TOOLS",
]
