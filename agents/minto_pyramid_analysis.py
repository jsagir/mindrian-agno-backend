"""
Minto Pyramid Analysis Agents

Auto-generated from skill package: minto-pyramid-analysis
Version: 1.0.0

Complete SCQA/MECE pyramid analysis with evidence gathering and synthesis
"""

import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.db.sqlite import AsyncSqliteDb

from tools.minto_pyramid_analysis_tools import (
    critique_pyramid, develop_scqa_framework, finalize_pyramid, gather_minto_evidence, generate_mece_framework, initialize_minto_analysis, search_pws_knowledge, synthesize_pyramid
)

# Optional: PWS Brain integration
try:
    from agents.larry import PWS_TOOLS, OPPORTUNITY_TOOLS, pws_knowledge
except ImportError:
    PWS_TOOLS = []
    OPPORTUNITY_TOOLS = []
    pws_knowledge = None


# =============================================================================
# MODEL CONFIGURATION
# =============================================================================

def get_gemini_model():
    """Get Gemini model with API key."""
    return Gemini(
        id="gemini-2.5-flash-preview-05-20",
        api_key=os.getenv("GOOGLE_AI_API_KEY"),
    )


# Shared database
mindrian_db = AsyncSqliteDb(db_file="mindrian.db", session_table="minto_pyramid_analysis_sessions")


# =============================================================================
# AGENTS
# =============================================================================

minto_analyst = Agent(
    name="Minto Analyst",
    id="minto-analyst",
    model=get_gemini_model(),
    instructions=["""# Minto Analyst

You are an expert in the Minto Pyramid Principle and SCQA framework.

## Your Expertise

- **SCQA Framework**: Situation → Complication → Question → Answer
- **MECE Structuring**: Mutually Exclusive, Collectively Exhaustive groupings
- **Pyramid Logic**: Top-down communication with supporting evidence

## Process

1. Start with SCQA - especially the Complication (the paradox/tension)
2. Build MECE groups - test for overlaps and gaps
3. Gather evidence - ground claims in research
4. Synthesize pyramid - deliver structured output

## Quality Standards

- SCQA must reveal opportunity, not prescribe solution
- Complication should be a genuine paradox or tension
- MECE groups must pass: No overlaps? Covers everything?
- Evidence must have proper citations"""],
    tools=[initialize_minto_analysis, develop_scqa_framework, generate_mece_framework, gather_minto_evidence, search_pws_knowledge],
    markdown=True,
    db=mindrian_db,
    description="Expert in SCQA/MECE structured thinking and pyramid analysis",
    reasoning=True,
    stream_intermediate_steps=True,
)
# Handoff Triggers:
#   - When SCQA and MECE frameworks are complete and validated -> minto-synthesizer
#   - When user requests critical review -> minto-critic



minto_synthesizer = Agent(
    name="Minto Synthesizer",
    id="minto-synthesizer",
    model=get_gemini_model(),
    instructions=["""# Minto Synthesizer

You synthesize SCQA frameworks, MECE structures, and evidence into polished pyramid deliverables.

## Your Role

- Take validated frameworks from the Minto Analyst
- Integrate evidence with proper citations
- Produce clear, actionable pyramid output
- Ensure logical flow from top to bottom

## Output Quality

- Clear governing thought at the top
- MECE groupings that support the main point
- Evidence properly attributed
- Implications clearly stated"""],
    tools=[synthesize_pyramid, finalize_pyramid],
    markdown=True,
    db=mindrian_db,
    description="Synthesizes frameworks and evidence into final pyramid deliverable",
    reasoning=True,
    stream_intermediate_steps=True,
)
# Handoff Triggers:
#   - When synthesis is complete -> minto-critic



minto_critic = Agent(
    name="Minto Critic",
    id="minto-critic",
    model=get_gemini_model(),
    instructions=["""# Minto Critic

You evaluate Minto pyramids against strict quality criteria.

## Evaluation Criteria

1. **SCQA Quality**
   - Is the Situation clear and relevant?
   - Does the Complication reveal genuine tension?
   - Does the Question open opportunity space?

2. **MECE Quality**
   - Are categories mutually exclusive (no overlaps)?
   - Are they collectively exhaustive (no gaps)?
   - Is the grouping logical?

3. **Evidence Quality**
   - Are claims supported by evidence?
   - Are citations provided?
   - Is evidence current and relevant?

4. **Logic Flow**
   - Does top-down logic hold?
   - Are conclusions warranted?

## Output

Provide:
- Score (0-100)
- Specific weaknesses
- Improvement suggestions
- GO / REVISE recommendation"""],
    tools=[critique_pyramid],
    markdown=True,
    db=mindrian_db,
    description="Reviews pyramid quality against Minto rubric",
    reasoning=True,
    stream_intermediate_steps=True,
)
# Handoff Triggers:
#   - When revision is needed (score < 70) -> minto-analyst



# =============================================================================
# REGISTRY
# =============================================================================

MINTO_PYRAMID_ANALYSIS_AGENTS = {
    "minto-analyst": minto_analyst,
    "minto-synthesizer": minto_synthesizer,
    "minto-critic": minto_critic
}


def get_minto_pyramid_analysis_agent(agent_id: str) -> Agent:
    """Get an agent by ID."""
    return MINTO_PYRAMID_ANALYSIS_AGENTS.get(agent_id)


def list_minto_pyramid_analysis_agents() -> list[dict]:
    """List all agents in this skill."""
    return [
        {
                "id": "minto-analyst",
                "name": "Minto Analyst",
                "role": "primary",
                "description": "Expert in SCQA/MECE structured thinking and pyramid analysis"
        },
        {
                "id": "minto-synthesizer",
                "name": "Minto Synthesizer",
                "role": "synthesizer",
                "description": "Synthesizes frameworks and evidence into final pyramid deliverable"
        },
        {
                "id": "minto-critic",
                "name": "Minto Critic",
                "role": "critic",
                "description": "Reviews pyramid quality against Minto rubric"
        }
]
