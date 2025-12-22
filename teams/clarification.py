"""
Clarification Team

A coordinated team of Larry the Clarifier and Larry the Devil's Advocate.
Used for initial problem exploration and assumption testing.

Flow:
1. Clarifier asks questions (max 5)
2. Devil challenges assumptions
3. Synthesizer organizes insights
"""

import os
from agno.team import Team
from agno.models.google import Gemini

from agents.larry import larry_clarifier, larry_devil, larry_synthesizer


# Clarification Team
clarification_team = Team(
    name="Clarification Team",
    description="Clarifies problems through questioning and challenge",
    model=Gemini(id="gemini-2.5-flash-preview-05-20", api_key=os.getenv("GOOGLE_AI_API_KEY")),
    members=[larry_clarifier, larry_devil, larry_synthesizer],
    instructions=[
        """
        ## Clarification Team Protocol

        This team helps users clarify their innovation challenge.

        ### Flow
        1. **Larry the Clarifier** asks up to 5 questions to understand:
           - What is the problem?
           - Who is affected?
           - What does success look like?

        2. **Larry the Devil's Advocate** challenges:
           - Hidden assumptions
           - Market realities
           - Execution risks

        3. **Larry the Synthesizer** organizes:
           - SCQA structure
           - Key insights
           - Next steps

        ### Success Criteria
        - Problem is clearly stated (one sentence)
        - Target audience is identified
        - Success criteria are defined
        - Major assumptions are surfaced
        - A Minto Pyramid synthesis is produced
        """,
    ],
    markdown=True,
)
