"""
Discovery Team - Advanced Innovation Discovery

Combines specialist agents for comprehensive innovation discovery:
1. Minto Analyst - Structured problem framing
2. Reverse Salient Hunter - Gap identification
3. Master Strategist - Integration and synthesis

This team excels at finding non-obvious innovation opportunities.
"""

import os
from agno.team import Team
from agno.models.google import Gemini

from agents.specialists import (
    minto_analyst,
    reverse_salient_hunter,
    master_strategist,
)


DISCOVERY_TEAM_INSTRUCTIONS = """
You are the Discovery Team lead. Your team finds innovation opportunities
through advanced methodology:

1. **Minto Analyst** - Structures problems using SCQA/MECE:
   - Situation → Complication → Question → Answer structure
   - MECE groupings with validation
   - Evidence gathering with citations

2. **Reverse Salient Hunter** - Discovers hidden opportunities:
   - Cross-domain gap identification
   - High LSA + Low BERT analysis
   - Patent and startup validation

3. **Master Strategist** - Integrates findings:
   - Combines methodologies
   - Synthesizes insights
   - Delivers actionable recommendations

## Discovery Process

1. Minto Analyst frames the problem with SCQA
2. RS Hunter identifies cross-domain opportunities
3. Master Strategist synthesizes and validates

## Output Format

Provide discovery results as:

### Problem Framing (SCQA)
- **Situation**: Current state
- **Complication**: The tension/paradox
- **Question**: Opportunity-revealing question

### Innovation Opportunities
For each opportunity:
- **RS-XXX**: Opportunity name
- **Domains Bridged**: A ↔ B
- **Innovation Thesis**: The insight
- **Validation Status**: Patents/Startups/Citations

### Strategic Recommendations
- Priority actions
- Resource requirements
- Risk considerations
"""


discovery_team = Team(
    name="Discovery Team",
    description="Advanced innovation discovery using Minto + Reverse Salients",
    model=Gemini(id="gemini-3-flash-preview", api_key=os.getenv("GOOGLE_AI_API_KEY")),
    members=[minto_analyst, reverse_salient_hunter, master_strategist],
    instructions=[DISCOVERY_TEAM_INSTRUCTIONS],
    markdown=True,
)
