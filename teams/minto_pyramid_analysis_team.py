"""
Minto Pyramid Analysis Team

Auto-generated from skill package: minto-pyramid-analysis
Version: 1.0.0
"""

import os
from agno.team import Team
from agno.models.google import Gemini

from agents.minto_pyramid_analysis import (
    minto_analyst, minto_synthesizer, minto_critic
)


# =============================================================================
# TEAM CONFIGURATION
# =============================================================================

minto_pyramid_analysis_team = Team(
    name="Minto Analysis Team",
    description="Complete SCQA/MECE pyramid analysis with evidence gathering and synthesis",
    model=Gemini(id="gemini-3-flash-preview", api_key=os.getenv("GOOGLE_AI_API_KEY")),
    members=[minto_analyst, minto_synthesizer, minto_critic],
    instructions=["""


## Success Criteria
Pyramid passes quality review with score >= 70
"""],
    markdown=True,
)

