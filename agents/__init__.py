"""
Mindrian Agents Package
All Agno agents for the Mindrian platform.

Includes:
- Larry Agents: 7 conversational roles for innovation guidance
- Specialists: 4 advanced agents with FastMCP cloud tools
"""

from agents.larry import (
    larry_clarifier,
    larry_coach,
    larry_expert,
    larry_devil,
    larry_synthesizer,
    larry_teacher,
    larry_pws_instructor,
    LARRY_AGENTS,
    get_agent,
    list_agents,
)

from agents.specialists import (
    minto_analyst,
    reverse_salient_hunter,
    data_extractor,
    master_strategist,
    SPECIALIST_AGENTS,
    get_specialist,
    list_specialists,
)

__all__ = [
    # Larry Agents
    "larry_clarifier",
    "larry_coach",
    "larry_expert",
    "larry_devil",
    "larry_synthesizer",
    "larry_teacher",
    "larry_pws_instructor",
    "LARRY_AGENTS",
    "get_agent",
    "list_agents",
    # Specialists
    "minto_analyst",
    "reverse_salient_hunter",
    "data_extractor",
    "master_strategist",
    "SPECIALIST_AGENTS",
    "get_specialist",
    "list_specialists",
]
