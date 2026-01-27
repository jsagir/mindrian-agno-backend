"""
Analysis Team

A collaborative team for applying PWS frameworks to problems.
Multiple agents work together to analyze from different perspectives.

Members:
- PWS Instructor (hands-on methodology)
- Expert (domain knowledge)
- Coach (structured guidance)
"""

import os
from agno.team import Team
from agno.models.google import Gemini

from agents.larry import larry_pws_instructor, larry_expert, larry_coach


# Analysis Team
analysis_team = Team(
    name="Analysis Team",
    description="Applies PWS frameworks to analyze problems",
    model=Gemini(id="gemini-3-flash-preview", api_key=os.getenv("GOOGLE_AI_API_KEY")),
    members=[larry_pws_instructor, larry_expert, larry_coach],
    instructions=[
        """
        ## Analysis Team Protocol

        This team applies PWS frameworks to the user's challenge.

        ### Framework Selection
        Based on problem type, select appropriate frameworks:

        **For Customer Understanding:**
        - Jobs to Be Done (JTBD)
        - Four Lenses of Innovation

        **For Market Analysis:**
        - White Space Mapping
        - S-Curve Analysis

        **For Future Planning:**
        - Scenario Analysis (2x2 Matrix)
        - Trending to Absurd

        **For Validation:**
        - PWS Validation Scorecard
        - Minto Pyramid

        ### Team Contributions

        **PWS Instructor** - Runs the framework step-by-step
        - Provides hands-on guidance
        - Ensures correct methodology
        - Generates framework outputs

        **Expert** - Provides domain context
        - Connects frameworks to user's industry
        - Shares relevant examples
        - Warns of common pitfalls

        **Coach** - Keeps progress moving
        - Tracks what's been covered
        - Identifies next steps
        - Maintains momentum

        ### Output Format
        - Framework output (JTBD map, Scorecard, etc.)
        - Key insights
        - Actionable next steps
        """,
    ],
    markdown=True,
)
