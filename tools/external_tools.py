"""
External Service Tools - Direct API Integration for Gemini

These tools connect directly to external services without MCP,
so Gemini and other non-Claude models can use them.

Services:
1. Tavily - Web search and research
2. Neo4j - Knowledge graph queries
3. Pinecone - Vector search (PWS Brain)
"""

import os
from typing import Optional, List, Dict, Any
from agno.tools import tool


# =============================================================================
# TAVILY WEB SEARCH
# =============================================================================

@tool
def tavily_search(
    query: str,
    search_depth: str = "advanced",
    max_results: int = 10,
    include_domains: List[str] = None,
    exclude_domains: List[str] = None,
    topic: str = "general"
) -> str:
    """
    Search the web using Tavily API for real-time information.

    Use this tool when you need:
    - Current news and events
    - Research on specific topics
    - Market/competitor information
    - Technical documentation
    - Academic papers and citations

    Args:
        query: The search query
        search_depth: "basic" (fast) or "advanced" (comprehensive)
        max_results: Number of results (1-20)
        include_domains: Only search these domains (e.g., ["arxiv.org", "nature.com"])
        exclude_domains: Exclude these domains
        topic: "general" or "news"

    Returns:
        Formatted search results with titles, snippets, and URLs

    Example:
        tavily_search("jobs to be done framework examples 2024")
        tavily_search("AI healthcare startups", topic="news", max_results=5)
    """
    try:
        from tavily import TavilyClient

        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "Error: TAVILY_API_KEY not set. Add it to your environment variables."

        client = TavilyClient(api_key=api_key)

        # Build search parameters
        params = {
            "query": query,
            "search_depth": search_depth,
            "max_results": min(max_results, 20),
            "topic": topic,
        }

        if include_domains:
            params["include_domains"] = include_domains
        if exclude_domains:
            params["exclude_domains"] = exclude_domains

        # Execute search
        response = client.search(**params)

        # Format results
        results = response.get("results", [])
        if not results:
            return f"No results found for: {query}"

        output = [f"## Web Search: {query}\n"]
        output.append(f"*{len(results)} results from Tavily*\n")

        for i, result in enumerate(results, 1):
            title = result.get("title", "Untitled")
            url = result.get("url", "")
            snippet = result.get("content", "")[:500]
            score = result.get("score", 0)

            output.append(f"### {i}. {title}")
            output.append(f"**URL**: {url}")
            output.append(f"**Relevance**: {score:.2f}")
            output.append(f"\n{snippet}\n")
            output.append("---")

        return "\n".join(output)

    except ImportError:
        return "Error: tavily package not installed. Run: pip install tavily-python"
    except Exception as e:
        return f"Error searching Tavily: {str(e)}"


@tool
def tavily_extract(url: str) -> str:
    """
    Extract and summarize content from a URL using Tavily.

    Use this when you need to:
    - Get full content from an article
    - Extract information from a webpage
    - Summarize a long document

    Args:
        url: The URL to extract content from

    Returns:
        Extracted and cleaned content from the URL
    """
    try:
        from tavily import TavilyClient

        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "Error: TAVILY_API_KEY not set"

        client = TavilyClient(api_key=api_key)
        response = client.extract(urls=[url])

        results = response.get("results", [])
        if not results:
            return f"Could not extract content from: {url}"

        content = results[0].get("raw_content", "No content extracted")
        return f"## Extracted from {url}\n\n{content}"

    except Exception as e:
        return f"Error extracting from URL: {str(e)}"


# =============================================================================
# NEO4J KNOWLEDGE GRAPH
# =============================================================================

def _get_neo4j_driver():
    """Get Neo4j driver with connection handling."""
    from neo4j import GraphDatabase

    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "")

    if not password:
        raise ValueError("NEO4J_PASSWORD not set")

    return GraphDatabase.driver(uri, auth=(user, password))


@tool
def neo4j_query(cypher: str, params: Dict[str, Any] = None) -> str:
    """
    Execute a read-only Cypher query on the Neo4j knowledge graph.

    Use this to:
    - Query the knowledge graph for insights
    - Find relationships between concepts
    - Explore stored opportunities
    - Search for patterns in data

    Args:
        cypher: Cypher query (READ-ONLY - no CREATE/DELETE/MERGE)
        params: Query parameters as dict

    Returns:
        Query results formatted as markdown

    Example:
        neo4j_query("MATCH (o:Opportunity) RETURN o.title, o.status LIMIT 10")
        neo4j_query("MATCH (n)-[r]->(m) RETURN type(r), count(*) as count")
    """
    try:
        # Security: Block write operations
        cypher_upper = cypher.upper()
        write_keywords = ["CREATE", "DELETE", "MERGE", "SET", "REMOVE", "DROP"]
        for keyword in write_keywords:
            if keyword in cypher_upper:
                return f"Error: Write operations not allowed. Use dedicated tools for mutations."

        driver = _get_neo4j_driver()

        with driver.session() as session:
            result = session.run(cypher, params or {})
            records = list(result)

        driver.close()

        if not records:
            return "Query returned no results."

        # Format as markdown table
        keys = records[0].keys()
        output = ["## Query Results\n"]
        output.append("| " + " | ".join(keys) + " |")
        output.append("| " + " | ".join(["---"] * len(keys)) + " |")

        for record in records[:50]:  # Limit to 50 rows
            values = [str(record[k])[:100] for k in keys]  # Truncate long values
            output.append("| " + " | ".join(values) + " |")

        if len(records) > 50:
            output.append(f"\n*Showing 50 of {len(records)} results*")

        return "\n".join(output)

    except ValueError as e:
        return f"Configuration error: {str(e)}"
    except Exception as e:
        return f"Error querying Neo4j: {str(e)}"


@tool
def neo4j_get_schema() -> str:
    """
    Get the schema of the Neo4j knowledge graph.

    Returns information about:
    - Node labels and their properties
    - Relationship types
    - Indexes and constraints

    Use this to understand what data is available before querying.
    """
    try:
        driver = _get_neo4j_driver()

        output = ["## Neo4j Knowledge Graph Schema\n"]

        with driver.session() as session:
            # Get node labels and counts
            result = session.run("""
                CALL db.labels() YIELD label
                CALL apoc.cypher.run('MATCH (n:`' + label + '`) RETURN count(n) as count', {})
                YIELD value
                RETURN label, value.count as count
                ORDER BY count DESC
            """)

            output.append("### Node Labels")
            output.append("| Label | Count |")
            output.append("| --- | --- |")
            for record in result:
                output.append(f"| {record['label']} | {record['count']} |")

            # Get relationship types
            result = session.run("""
                CALL db.relationshipTypes() YIELD relationshipType
                RETURN relationshipType
            """)

            output.append("\n### Relationship Types")
            for record in result:
                output.append(f"- `{record['relationshipType']}`")

        driver.close()
        return "\n".join(output)

    except Exception as e:
        return f"Error getting schema: {str(e)}"


@tool
def neo4j_save_insight(
    title: str,
    content: str,
    insight_type: str = "general",
    source: str = "mindrian",
    tags: List[str] = None
) -> str:
    """
    Save an insight to the knowledge graph.

    Use this to persist valuable discoveries:
    - Key findings from analysis
    - Innovation opportunities
    - Framework applications
    - User learnings

    Args:
        title: Short title for the insight
        content: Full insight content
        insight_type: Type (general, opportunity, framework, discovery)
        source: Where this came from
        tags: List of tags for categorization

    Returns:
        Confirmation with insight ID
    """
    try:
        from datetime import datetime

        driver = _get_neo4j_driver()
        insight_id = f"insight-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        cypher = """
        CREATE (i:Insight {
            id: $id,
            title: $title,
            content: $content,
            type: $type,
            source: $source,
            tags: $tags,
            created_at: datetime()
        })
        RETURN i.id as id
        """

        with driver.session() as session:
            result = session.run(cypher, {
                "id": insight_id,
                "title": title,
                "content": content,
                "type": insight_type,
                "source": source,
                "tags": tags or []
            })
            record = result.single()

        driver.close()

        return f"✅ Insight saved!\n- **ID**: {insight_id}\n- **Title**: {title}\n- **Type**: {insight_type}"

    except Exception as e:
        return f"Error saving insight: {str(e)}"


# =============================================================================
# PINECONE VECTOR SEARCH (Enhanced)
# =============================================================================

@tool
def pinecone_search(
    query: str,
    index_name: str = "neo4j-knowledge-base",
    top_k: int = 5,
    namespace: str = "",
    filter_metadata: Dict[str, Any] = None
) -> str:
    """
    Search any Pinecone index for similar content.

    Available indexes:
    - neo4j-knowledge-base: Primary knowledge (multilingual-e5-large)
    - pws-world: PWS course content

    Args:
        query: Search query text
        index_name: Which index to search
        top_k: Number of results (1-20)
        namespace: Pinecone namespace (optional)
        filter_metadata: Filter by metadata fields

    Returns:
        Matching documents with relevance scores
    """
    try:
        from pinecone import Pinecone

        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            return "Error: PINECONE_API_KEY not set"

        pc = Pinecone(api_key=api_key)

        # Index configurations
        index_configs = {
            "neo4j-knowledge-base": {
                "host": "https://neo4j-knowledge-base-bc1849d.svc.aped-4627-b74a.pinecone.io",
            },
            "pws-world": {
                "host": None,  # Use default
            }
        }

        config = index_configs.get(index_name, {})

        if config.get("host"):
            index = pc.Index(host=config["host"])
        else:
            index = pc.Index(index_name)

        # Build search query
        search_params = {
            "namespace": namespace,
            "query": {
                "inputs": {"text": query},
                "top_k": min(top_k, 20)
            },
            "include_metadata": True
        }

        if filter_metadata:
            search_params["filter"] = filter_metadata

        results = index.search(**search_params)

        # Format results
        matches = getattr(results, 'matches', []) or results.get("matches", [])

        if not matches:
            return f"No matches found for: {query}"

        output = [f"## Vector Search: {query}\n"]
        output.append(f"*Index: {index_name} | {len(matches)} matches*\n")

        for i, match in enumerate(matches, 1):
            score = getattr(match, 'score', match.get('score', 0))
            metadata = getattr(match, 'metadata', match.get('metadata', {})) or {}

            title = metadata.get("title", metadata.get("name", "Untitled"))
            content = metadata.get("text", metadata.get("content", ""))[:400]
            source = metadata.get("source", metadata.get("type", ""))

            output.append(f"### {i}. {title}")
            output.append(f"**Score**: {score:.3f}")
            if source:
                output.append(f"**Source**: {source}")
            output.append(f"\n{content}\n")
            output.append("---")

        return "\n".join(output)

    except Exception as e:
        return f"Error searching Pinecone: {str(e)}"


@tool
def pinecone_list_indexes() -> str:
    """
    List all available Pinecone indexes and their stats.

    Returns information about each index:
    - Name and dimensions
    - Vector count
    - Namespaces
    """
    try:
        from pinecone import Pinecone

        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            return "Error: PINECONE_API_KEY not set"

        pc = Pinecone(api_key=api_key)
        indexes = pc.list_indexes()

        output = ["## Pinecone Indexes\n"]

        for idx in indexes:
            name = idx.name if hasattr(idx, 'name') else idx.get('name', 'unknown')
            output.append(f"### {name}")

            # Get stats
            try:
                index = pc.Index(name)
                stats = index.describe_index_stats()
                total = stats.get("total_vector_count", 0)
                dims = stats.get("dimension", "unknown")
                output.append(f"- **Vectors**: {total:,}")
                output.append(f"- **Dimensions**: {dims}")
            except:
                output.append("- *Could not fetch stats*")

            output.append("")

        return "\n".join(output)

    except Exception as e:
        return f"Error listing indexes: {str(e)}"


# =============================================================================
# TOOL COLLECTIONS
# =============================================================================

TAVILY_TOOLS = [
    tavily_search,
    tavily_extract,
]

NEO4J_TOOLS = [
    neo4j_query,
    neo4j_get_schema,
    neo4j_save_insight,
]

PINECONE_TOOLS = [
    pinecone_search,
    pinecone_list_indexes,
]

ALL_EXTERNAL_TOOLS = TAVILY_TOOLS + NEO4J_TOOLS + PINECONE_TOOLS
