"""
Mindrian Teams Package
Coordinated multi-agent teams for complex tasks.

Teams:
- Clarification Team: Larry Clarifier + Devil's Advocate + Synthesizer
- Analysis Team: PWS Instructor + Expert + Coach
- Validation Team: PWS Instructor + Devil + Expert
- Exploration Team: Clarifier + Teacher + Synthesizer
- Discovery Team: Minto Analyst + RS Hunter + Master Strategist
"""

from teams.clarification import clarification_team
from teams.analysis import analysis_team
from teams.validation import validation_team
from teams.exploration import exploration_team
from teams.discovery import discovery_team

ALL_TEAMS = {
    "clarification": clarification_team,
    "analysis": analysis_team,
    "validation": validation_team,
    "exploration": exploration_team,
    "discovery": discovery_team,
}


def get_team(name: str):
    """Get a team by name."""
    return ALL_TEAMS.get(name, clarification_team)


def list_teams() -> list[dict]:
    """List all available teams with metadata."""
    return [
        {
            "id": "clarification",
            "name": "Clarification Team",
            "description": "Clarifies problems through questioning and challenge",
            "members": ["Clarifier", "Devil's Advocate", "Synthesizer"],
        },
        {
            "id": "analysis",
            "name": "Analysis Team",
            "description": "Applies PWS frameworks to analyze problems",
            "members": ["PWS Instructor", "Expert", "Coach"],
        },
        {
            "id": "validation",
            "name": "Validation Team",
            "description": "Validates opportunities through PWS, Devil's Advocate, and Expert",
            "members": ["PWS Instructor", "Devil's Advocate", "Expert"],
        },
        {
            "id": "exploration",
            "name": "Exploration Team",
            "description": "Explores possibilities through questioning and synthesis",
            "members": ["Clarifier", "Teacher", "Synthesizer"],
        },
        {
            "id": "discovery",
            "name": "Discovery Team",
            "description": "Advanced innovation discovery using Minto + Reverse Salients",
            "members": ["Minto Analyst", "RS Hunter", "Master Strategist"],
        },
    ]


__all__ = [
    "clarification_team",
    "analysis_team",
    "validation_team",
    "exploration_team",
    "discovery_team",
    "ALL_TEAMS",
    "get_team",
    "list_teams",
]
