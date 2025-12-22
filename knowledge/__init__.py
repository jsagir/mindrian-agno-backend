"""
Mindrian Knowledge Base

Pinecone-powered RAG for PWS course content and conversation context.
"""

import os
from agno.vectordb.pineconedb import PineconeDb
from agno.knowledge import Knowledge
from agno.knowledge.embedder.openai import OpenAIEmbedder
from pinecone import ServerlessSpec


def get_pws_knowledge_base():
    """
    Create PWS Knowledge Base using Pinecone.

    Uses the existing pws-world index with 1024-dimensional embeddings.
    """
    api_key = os.getenv("PINECONE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("WARNING: PINECONE_API_KEY not set. Knowledge base disabled.")
        return None

    # Create embedder matching the index (text-embedding-3-large = 1024 dims)
    embedder = OpenAIEmbedder(
        id="text-embedding-3-large",
        dimensions=1024,
        api_key=openai_key,
    ) if openai_key else None

    # Connect to existing pws-world index
    pws_vectordb = PineconeDb(
        name="pws-world",
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        api_key=api_key,
        embedder=embedder,
        use_hybrid_search=False,
    )

    # Create knowledge base
    pws_knowledge = Knowledge(
        name="PWS Course Knowledge",
        description="Problem Worth Solving course content including JTBD, Minto, S-Curve, and other innovation frameworks",
        vector_db=pws_vectordb,
        max_results=5,
    )

    return pws_knowledge


# Export
__all__ = ["get_pws_knowledge_base"]
