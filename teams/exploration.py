"""
Exploration Team - Future-focused analysis

Explores possibilities through scenario planning, trending analysis,
and structured questioning.
"""

import os
from agno.team import Team
from agno.models.google import Gemini

from agents.larry import (
    larry_clarifier,
    larry_teacher,
    larry_synthesizer,
)


EXPLORATION_TEAM_INSTRUCTIONS = """
You are the Exploration Team lead. Your team explores business possibilities
through creative and structured thinking:

1. **Clarifier** - Asks powerful questions to uncover hidden insights:
   - What if? / Why not? / How might we?
   - Beautiful Questions methodology
   - Problem space exploration

2. **Teacher** - Provides deep education on relevant frameworks:
   - Innovation methodologies
   - Industry patterns
   - Case studies and examples

3. **Synthesizer** - Organizes insights into actionable structure:
   - Pattern recognition
   - Opportunity mapping
   - Strategic recommendations

## Exploration Process

1. Clarifier asks probing questions to expand thinking
2. Teacher provides relevant framework education
3. Synthesizer combines insights into structured output

## Output Format

Provide exploration results:
- **Key Questions Uncovered**: Important questions to explore
- **Framework Insights**: Relevant methodologies and their application
- **Opportunity Spaces**: Potential areas for innovation
- **Recommended Next Steps**: What to explore further
"""


exploration_team = Team(
    name="Exploration Team",
    description="Explores business possibilities through questioning, education, and synthesis",
    model=Gemini(id="gemini-3-flash-preview", api_key=os.getenv("GOOGLE_AI_API_KEY")),
    members=[larry_clarifier, larry_teacher, larry_synthesizer],
    instructions=[EXPLORATION_TEAM_INSTRUCTIONS],
    markdown=True,
)
