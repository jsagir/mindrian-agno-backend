"""
Mindrian Handoff System

Structured handoff framework for multi-agent coordination.
Enables context-aware agent delegation and returns.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, List, Any
from datetime import datetime


class HandoffType(Enum):
    """Types of agent handoffs."""
    DELEGATE = "delegate"      # Larry assigns work, receives results
    TRANSFER = "transfer"      # Full control passes to another agent
    RETURN = "return"          # Framework completes, results return to Larry


class HandoffMode(Enum):
    """Execution modes for handoffs."""
    SEQUENTIAL = "sequential"  # Agents build progressively
    PARALLEL = "parallel"      # Multiple independent analyses
    DEBATE = "debate"          # Adversarial positions with synthesis


@dataclass
class ProblemClarity:
    """Tracks problem definition clarity."""
    what: str = ""              # What is the problem?
    who: str = ""               # Who has this problem?
    success: str = ""           # What does success look like?
    what_score: float = 0.0     # Clarity score 0-1
    who_score: float = 0.0
    success_score: float = 0.0

    @property
    def overall_score(self) -> float:
        """Calculate overall clarity score."""
        return (self.what_score + self.who_score + self.success_score) / 3

    @property
    def is_clear(self) -> bool:
        """Check if problem is sufficiently clear."""
        return self.overall_score >= 0.7


@dataclass
class HandoffContext:
    """
    Structured context for agent handoffs.

    Instead of passing entire conversation histories, we pass
    structured, problem-focused context that enables clearer
    delegation and more reliable synthesis.
    """
    # Problem Definition
    problem_what: str = ""
    problem_who: str = ""
    problem_success: str = ""
    problem_clarity: Optional[ProblemClarity] = None

    # Conversation Summary (not full history)
    conversation_summary: str = ""
    key_constraints: List[str] = field(default_factory=list)
    user_preferences: Dict[str, Any] = field(default_factory=dict)

    # Previous Analyses (structured results)
    previous_analyses: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # Task Instructions
    task_description: str = ""
    expected_output: str = ""
    focus_areas: List[str] = field(default_factory=list)

    # Metadata
    session_id: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_prompt_context(self) -> str:
        """Convert to prompt-ready context string."""
        parts = []

        if self.problem_what:
            parts.append(f"**Problem (What):** {self.problem_what}")
        if self.problem_who:
            parts.append(f"**Target User (Who):** {self.problem_who}")
        if self.problem_success:
            parts.append(f"**Success Criteria:** {self.problem_success}")

        if self.conversation_summary:
            parts.append(f"\n**Context:** {self.conversation_summary}")

        if self.key_constraints:
            parts.append(f"\n**Constraints:** {', '.join(self.key_constraints)}")

        if self.previous_analyses:
            parts.append("\n**Previous Analyses:**")
            for name, result in self.previous_analyses.items():
                parts.append(f"- {name}: {result.get('summary', 'No summary')}")

        if self.task_description:
            parts.append(f"\n**Your Task:** {self.task_description}")

        if self.expected_output:
            parts.append(f"**Expected Output:** {self.expected_output}")

        return "\n".join(parts)


@dataclass
class Handoff:
    """Represents a handoff between agents."""
    type: HandoffType
    from_agent: str
    to_agent: str
    context: HandoffContext
    mode: HandoffMode = HandoffMode.SEQUENTIAL
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "type": self.type.value,
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "mode": self.mode.value,
            "context": {
                "problem_what": self.context.problem_what,
                "problem_who": self.context.problem_who,
                "conversation_summary": self.context.conversation_summary,
                "task_description": self.context.task_description,
            },
            "created_at": self.created_at,
        }


class HandoffManager:
    """
    Manages handoffs between agents.

    Provides tools for creating and routing handoffs,
    and tracking handoff history for analysis.
    """

    def __init__(self):
        self.handoff_history: List[Handoff] = []

    def create_handoff(
        self,
        type: HandoffType,
        from_agent: str,
        to_agent: str,
        context: HandoffContext,
        mode: HandoffMode = HandoffMode.SEQUENTIAL
    ) -> Handoff:
        """Create a new handoff."""
        handoff = Handoff(
            type=type,
            from_agent=from_agent,
            to_agent=to_agent,
            context=context,
            mode=mode
        )
        self.handoff_history.append(handoff)
        return handoff

    def get_history(self, session_id: str = None) -> List[Handoff]:
        """Get handoff history, optionally filtered by session."""
        if session_id:
            return [h for h in self.handoff_history
                    if h.context.session_id == session_id]
        return self.handoff_history

    def clear_history(self, session_id: str = None):
        """Clear handoff history."""
        if session_id:
            self.handoff_history = [h for h in self.handoff_history
                                    if h.context.session_id != session_id]
        else:
            self.handoff_history = []


# Global handoff manager instance
handoff_manager = HandoffManager()


def create_handoff(
    type: HandoffType,
    from_agent: str,
    to_agent: str,
    context: HandoffContext,
    mode: HandoffMode = HandoffMode.SEQUENTIAL
) -> Handoff:
    """Convenience function for creating handoffs."""
    return handoff_manager.create_handoff(type, from_agent, to_agent, context, mode)


# Export all public classes and functions
__all__ = [
    "HandoffType",
    "HandoffMode",
    "ProblemClarity",
    "HandoffContext",
    "Handoff",
    "HandoffManager",
    "handoff_manager",
    "create_handoff",
]
