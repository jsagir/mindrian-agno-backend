"""
PWS Brain Tools - Pinecone Integration for PWS Course Knowledge

This module provides tools for searching knowledge bases:
1. neo4j-knowledge-base - Primary RAG (multilingual-e5-large, 1024 dims)
2. pws-world - PWS course content fallback

Uses Pinecone's integrated inference for automatic embedding.
"""

import os
from typing import Optional
from pinecone import Pinecone

# Initialize Pinecone clients lazily
_pinecone_client: Optional[Pinecone] = None
_indexes = {}

# Index configurations
INDEX_CONFIGS = {
    "neo4j-knowledge-base": {
        "host": "https://neo4j-knowledge-base-bc1849d.svc.aped-4627-b74a.pinecone.io",
        "model": "multilingual-e5-large",
        "dimensions": 1024,
        "namespace": "",
        "priority": 1,  # Primary
    },
    "pws-world": {
        "model": "text-embedding-3-large",
        "dimensions": 1024,
        "namespace": "",
        "priority": 2,  # Fallback
    },
}

# Default index
DEFAULT_INDEX = os.getenv("PINECONE_INDEX_NAME", "neo4j-knowledge-base")


def _get_pinecone_client():
    """Get or initialize Pinecone client."""
    global _pinecone_client

    if _pinecone_client is None:
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY environment variable not set")
        _pinecone_client = Pinecone(api_key=api_key)

    return _pinecone_client


def _get_pinecone_index(index_name: str = None):
    """Get or initialize Pinecone index."""
    global _indexes

    index_name = index_name or DEFAULT_INDEX

    if index_name not in _indexes:
        pc = _get_pinecone_client()
        config = INDEX_CONFIGS.get(index_name, {})

        # Use host if provided, otherwise use index name
        if "host" in config:
            _indexes[index_name] = pc.Index(host=config["host"])
        else:
            _indexes[index_name] = pc.Index(index_name)

    return _indexes[index_name]


def search_knowledge(query: str, top_k: int = 5, index_name: str = None) -> str:
    """
    Search knowledge base for relevant content.

    Uses neo4j-knowledge-base (primary) with multilingual-e5-large embeddings.

    Args:
        query: The search query
        top_k: Number of results to return (default 5)
        index_name: Specific index to search (default: neo4j-knowledge-base)

    Returns:
        Formatted string with relevant knowledge chunks
    """
    try:
        index_name = index_name or DEFAULT_INDEX
        index = _get_pinecone_index(index_name)
        config = INDEX_CONFIGS.get(index_name, {})

        # Use Pinecone's integrated inference for search
        results = index.search(
            namespace=config.get("namespace", ""),
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
            matches = results.get("matches", results.get("results", []))
            if isinstance(matches, list) and len(matches) > 0 and isinstance(matches[0], dict) and "matches" in matches[0]:
                matches = matches[0]["matches"]

        if not matches:
            return f"No knowledge found for: {query}"

        output_parts = [f"## Knowledge Search: {query}\n"]
        output_parts.append(f"*Index: {index_name} | Model: {config.get('model', 'unknown')}*\n")

        for i, match in enumerate(matches, 1):
            if hasattr(match, 'score'):
                score = match.score
                metadata = match.metadata or {}
            else:
                score = match.get("score", 0)
                metadata = match.get("metadata", {})

            title = metadata.get("title", metadata.get("name", "Untitled"))
            content = metadata.get("text", metadata.get("content", metadata.get("description", "No content")))
            source = metadata.get("source", metadata.get("type", "Knowledge Base"))

            output_parts.append(f"### {i}. {title}")
            output_parts.append(f"**Relevance:** {score:.2f}")
            output_parts.append(f"\n{content}\n")
            output_parts.append(f"*Source: {source}*\n---")

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error searching knowledge: {str(e)}"


def search_pws_knowledge(query: str, top_k: int = 5) -> str:
    """
    Search PWS course knowledge base for relevant content.

    Use this tool when you need to:
    - Find PWS framework information (JTBD, Minto, S-Curve, etc.)
    - Ground your advice in actual course methodology
    - Answer questions about innovation frameworks
    - Provide citations from PWS materials

    Args:
        query: The search query (e.g., "jobs to be done framework", "minto pyramid example")
        top_k: Number of results to return (default 5)

    Returns:
        Formatted string with relevant PWS knowledge chunks
    """
    # Use primary knowledge base (neo4j-knowledge-base)
    return search_knowledge(query, top_k, DEFAULT_INDEX)


def get_framework_details(framework_name: str) -> str:
    """
    Get detailed information about a specific PWS framework.

    Use this tool when the user asks about specific frameworks:
    - Jobs to Be Done (JTBD)
    - Minto Pyramid / SCQA
    - S-Curve Analysis
    - Four Lenses of Innovation
    - White Space Mapping
    - Scenario Analysis
    - Devil's Advocate
    - And other PWS methodologies

    Args:
        framework_name: Name of the framework (e.g., "JTBD", "Minto Pyramid")

    Returns:
        Detailed framework information from PWS course
    """
    # Map common names to search terms
    framework_aliases = {
        "jtbd": "jobs to be done JTBD hire product progress",
        "jobs to be done": "jobs to be done JTBD milkshake hire",
        "minto": "minto pyramid SCQA situation complication question answer",
        "scqa": "SCQA situation complication question answer minto",
        "s-curve": "s-curve technology adoption lifecycle",
        "s curve": "s-curve technology adoption lifecycle",
        "four lenses": "four lenses innovation orthodoxies trends",
        "white space": "white space mapping opportunity gap",
        "scenario analysis": "scenario analysis 2x2 matrix future",
        "devil's advocate": "devil's advocate challenge assumptions stress test",
        "devils advocate": "devil's advocate challenge assumptions stress test",
    }

    # Get search term
    search_term = framework_aliases.get(
        framework_name.lower(),
        f"{framework_name} framework methodology PWS"
    )

    # Search with higher top_k for framework details
    return search_pws_knowledge(search_term, top_k=7)


# Framework definitions for when Pinecone is unavailable
FRAMEWORK_FALLBACKS = {
    "jtbd": """
## Jobs to Be Done (JTBD) Framework

The JTBD framework helps understand WHY customers buy products.

### Core Concept
Customers don't buy products - they HIRE them to make progress in their lives.

### The Milkshake Example
McDonald's discovered morning milkshakes were "hired" for:
- Long commute entertainment
- Satisfying breakfast
- Easy to consume while driving

The competition wasn't other milkshakes - it was bananas, bagels, and boredom.

### Three Job Types
1. **Functional Jobs**: What task needs to be done?
2. **Emotional Jobs**: How do they want to feel?
3. **Social Jobs**: How do they want to be perceived?

### Opportunity Formula
Opportunity = Importance x (1 - Satisfaction)

### Application
Ask: "What job would your product be hired for?"
""",
    "minto": """
## Minto Pyramid / SCQA Framework

A structured communication framework for clear thinking.

### SCQA Structure
- **Situation**: What's the context? (Facts everyone agrees on)
- **Complication**: What changed? (The problem or tension)
- **Question**: What needs answering? (The key question arising)
- **Answer**: What's the solution? (Your recommendation)

### Why It Works
- Leads with the answer (busy executives prefer this)
- Structures supporting arguments
- Creates logical flow

### Example
**S**: "We've been growing 20% annually"
**C**: "But growth slowed to 5% this quarter"
**Q**: "How do we reignite growth?"
**A**: "Enter the enterprise market with a new product line"
""",
}
