"""
PWS Brain Tools - Gemini File Search Integration for PWS Course Knowledge

This module provides tools for searching the PWS knowledge base using
Google's Gemini File Search API (grounded retrieval).

Store: fileSearchStores/pwsknowledgebase-a4rnz3u41lsn
~389 documents, ~2M tokens indexed

Cost: Storage FREE, Retrieval FREE, Embedding ~$0.30 one-time
"""

import os
from typing import Optional
from google import genai

# Gemini File Search Store ID
GEMINI_FILE_SEARCH_STORE = os.getenv(
    "GEMINI_FILE_SEARCH_STORE",
    "fileSearchStores/pwsknowledgebase-a4rnz3u41lsn"
)

# Initialize Gemini client lazily
_genai_client: Optional[genai.Client] = None


def _get_genai_client() -> genai.Client:
    """Get or initialize Gemini client."""
    global _genai_client

    if _genai_client is None:
        api_key = os.getenv("GOOGLE_AI_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_AI_API_KEY or GEMINI_API_KEY environment variable not set")
        _genai_client = genai.Client(api_key=api_key)

    return _genai_client


def search_knowledge(query: str, top_k: int = 5) -> str:
    """
    Search knowledge base using Gemini File Search (grounded retrieval).

    Args:
        query: The search query
        top_k: Number of results to return (used as guidance for retrieval)

    Returns:
        Formatted string with relevant knowledge chunks and grounding info
    """
    try:
        client = _get_genai_client()

        # Generate content with grounded retrieval using Gemini 3
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=f"""Search the PWS knowledge base and return the most relevant information for this query.

Query: {query}

Instructions:
- Return up to {top_k} relevant pieces of information
- Include specific details, frameworks, and examples from the knowledge base
- Cite which documents/sections the information comes from
- Format the response clearly with headers and bullet points""",
            config={
                "tools": [{"file_search": {"file_search_store_names": [GEMINI_FILE_SEARCH_STORE]}}],
                "temperature": 0.1,  # Low temp for factual retrieval
            }
        )

        # Extract text and grounding metadata
        result_text = response.text if hasattr(response, 'text') else str(response)

        # Check for grounding metadata (citations)
        output_parts = [f"## Knowledge Search: {query}\n"]
        output_parts.append(f"*Source: Gemini File Search | Store: pwsknowledgebase*\n")
        output_parts.append(result_text)

        # Add grounding chunks if available
        if hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                grounding = candidate.grounding_metadata
                if hasattr(grounding, 'grounding_chunks') and grounding.grounding_chunks:
                    output_parts.append("\n---\n### Source Documents:")
                    for i, chunk in enumerate(grounding.grounding_chunks[:top_k], 1):
                        if hasattr(chunk, 'retrieved_context'):
                            ctx = chunk.retrieved_context
                            title = getattr(ctx, 'title', f'Document {i}')
                            uri = getattr(ctx, 'uri', '')
                            output_parts.append(f"\n**{i}. {title}**")
                            if uri:
                                output_parts.append(f"  - URI: {uri}")

        return "\n".join(output_parts)

    except Exception as e:
        error_msg = str(e)
        # Provide fallback for common frameworks if search fails
        if "jtbd" in query.lower() or "jobs to be done" in query.lower():
            return FRAMEWORK_FALLBACKS.get("jtbd", f"Error searching knowledge: {error_msg}")
        elif "minto" in query.lower() or "scqa" in query.lower():
            return FRAMEWORK_FALLBACKS.get("minto", f"Error searching knowledge: {error_msg}")
        return f"Error searching knowledge: {error_msg}"


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
    return search_knowledge(query, top_k)


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
        "jtbd": "jobs to be done JTBD hire product progress milkshake example",
        "jobs to be done": "jobs to be done JTBD milkshake hire progress",
        "minto": "minto pyramid SCQA situation complication question answer structure",
        "scqa": "SCQA situation complication question answer minto pyramid",
        "s-curve": "s-curve technology adoption lifecycle innovation",
        "s curve": "s-curve technology adoption lifecycle",
        "four lenses": "four lenses innovation orthodoxies trends competencies",
        "white space": "white space mapping opportunity gap market",
        "scenario analysis": "scenario analysis 2x2 matrix future planning",
        "devil's advocate": "devil's advocate challenge assumptions stress test validation",
        "devils advocate": "devil's advocate challenge assumptions stress test",
        "reverse salient": "reverse salient bottleneck innovation opportunity",
        "4 pillar": "4 pillar validation scorecard market execution",
        "validation scorecard": "validation scorecard 4 pillar market execution team",
    }

    # Get search term
    search_term = framework_aliases.get(
        framework_name.lower(),
        f"{framework_name} framework methodology PWS innovation"
    )

    # Search with higher top_k for framework details
    return search_pws_knowledge(search_term, top_k=7)


# Framework definitions for fallback when API is unavailable
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
