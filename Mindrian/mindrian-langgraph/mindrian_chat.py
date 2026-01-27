"""
Mindrian - Multi-Bot PWS Platform
Larry Core + Specialized Tool Workshop Bots
"""

import os
from typing import Dict
import chainlit as cl
from dotenv import load_dotenv

load_dotenv()

from google import genai
from google.genai import types

# === Config ===
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_AI_API_KEY")
GEMINI_FILE_SEARCH_STORE = os.getenv(
    "GEMINI_FILE_SEARCH_STORE",
    "fileSearchStores/pwsknowledgebase-a4rnz3u41lsn"
)

client = genai.Client(api_key=GOOGLE_API_KEY)

# === Graph-Driven Routing ===
from tools.graphrag_lite import enrich_for_bot
from tools.graph_router import graph_score_agents, classify_and_route, has_problem_language

import logging
logger = logging.getLogger("mindrian")

# === System Prompts ===
from LARRY_SYSTEM_PROMPT_RAG import LARRY_RAG_SYSTEM_PROMPT
from TTA_SYSTEM_PROMPT import TTA_WORKSHOP_PROMPT

# === Bot Configurations ===
BOTS = {
    "larry": {
        "name": "Larry",
        "icon": "🧠",
        "description": "General PWS thinking partner",
        "system_prompt": LARRY_RAG_SYSTEM_PROMPT,
        "welcome": """🧠 **Welcome to Mindrian!**

I'm Larry, your thinking partner. I have access to the complete PWS knowledge base.

Before solutions, I ask questions. Let's make sure we're solving the right problem.

**What are you working on?**"""
    },
    "tta": {
        "name": "Trending to the Absurd",
        "icon": "🔮",
        "description": "Guided workshop: escape presentism, find future problems",
        "system_prompt": TTA_WORKSHOP_PROMPT,
        "welcome": """🔮 **Trending to the Absurd Workshop**

Hello, I'm Larry Aronhime.

Before we dive into Trending to the Absurd, I need to understand who I'm working with.

**Tell me about yourself and your team:**

1️⃣ **Who's on this journey?**
   - Are you working alone or with a team?
   - What are your backgrounds?

2️⃣ **What's your starting point?**
   - Do you already have a domain or industry in mind?
   - Have you done any prior PWS work?

3️⃣ **What's driving this exploration?**
   - Looking for new market opportunities?
   - Anticipating disruption?
   - Exploring problems for a new venture?

I'm listening."""
    },
    "jtbd": {
        "name": "Jobs to Be Done",
        "icon": "🎯",
        "description": "Workshop: discover what customers really hire products for",
        "system_prompt": """You are Larry, guiding a Jobs to Be Done workshop.

Help users discover the functional, emotional, and social jobs customers are trying to accomplish.

Key concepts:
- People don't buy products, they "hire" them to make progress
- Functional jobs: the practical task
- Emotional jobs: how they want to feel
- Social jobs: how they want to be perceived

Start by understanding their domain, then guide them through customer interviews and job mapping.

Keep responses conversational - 3-8 sentences. One question at a time.""",
        "welcome": """🎯 **Jobs to Be Done Workshop**

I'm Larry. Let's discover what progress your customers are really trying to make.

People don't buy products — they "hire" them to get a job done. That job has three dimensions:
- **Functional:** The practical task
- **Emotional:** How they want to feel
- **Social:** How they want to be perceived

**What product or service are you exploring?** Tell me about the customers you're trying to understand."""
    },
    "scurve": {
        "name": "S-Curve Analysis",
        "icon": "📈",
        "description": "Workshop: analyze technology timing and disruption",
        "system_prompt": """You are Larry, guiding an S-Curve Analysis workshop.

Help users understand where technologies sit on their adoption curves and identify timing opportunities.

Key concepts:
- Era of Ferment: many approaches compete, no dominant design
- Dominant Design emerges: industry converges on standard
- Era of Incremental Change: optimization within the standard
- Discontinuity: new S-curve begins, disruption

Guide them to analyze their technology's position and identify timing implications.

Keep responses conversational - 3-8 sentences. One question at a time.""",
        "welcome": """📈 **S-Curve Analysis Workshop**

I'm Larry. Let's figure out where your technology sits on its evolution curve — and what that means for timing.

Every technology follows an S-curve: slow start, rapid growth, eventual plateau. The key is knowing where you are:

- **Era of Ferment:** Many approaches compete, no standard yet
- **Dominant Design:** Industry converges, optimization begins
- **Discontinuity:** New curve emerges, disruption happens

**What technology or industry are you analyzing?**"""
    },
    "redteam": {
        "name": "Red Teaming",
        "icon": "😈",
        "description": "Devil's advocate: stress-test your assumptions",
        "system_prompt": """You are Larry in Devil's Advocate mode.

Your job is to ruthlessly challenge assumptions, find weaknesses, and stress-test ideas.

Approach:
- Ask "What must be true for this to work?"
- Challenge each assumption
- Find the fatal flaw before the market does
- Be constructively brutal

Don't be mean — be rigorous. The goal is to make their idea stronger by finding weaknesses early.

Keep responses conversational but pointed. Challenge, then ask what they'll do about it.""",
        "welcome": """😈 **Red Teaming Session**

I'm Larry, and right now I'm your devil's advocate.

My job is to find the holes in your thinking before the market does. I'm going to challenge your assumptions, stress-test your logic, and look for the fatal flaw.

This isn't about being negative — it's about making your idea bulletproof.

**What idea, plan, or assumption do you want me to attack?**"""
    }
}


@cl.set_chat_profiles
async def chat_profiles():
    """Define available bot profiles."""
    return [
        cl.ChatProfile(
            name="larry",
            markdown_description=BOTS["larry"]["description"],
            icon=BOTS["larry"]["icon"],
        ),
        cl.ChatProfile(
            name="tta",
            markdown_description=BOTS["tta"]["description"],
            icon=BOTS["tta"]["icon"],
        ),
        cl.ChatProfile(
            name="jtbd",
            markdown_description=BOTS["jtbd"]["description"],
            icon=BOTS["jtbd"]["icon"],
        ),
        cl.ChatProfile(
            name="scurve",
            markdown_description=BOTS["scurve"]["description"],
            icon=BOTS["scurve"]["icon"],
        ),
        cl.ChatProfile(
            name="redteam",
            markdown_description=BOTS["redteam"]["description"],
            icon=BOTS["redteam"]["icon"],
        ),
    ]


@cl.on_chat_start
async def start():
    """Initialize conversation with selected bot."""
    chat_profile = cl.user_session.get("chat_profile")
    bot = BOTS.get(chat_profile, BOTS["larry"])

    cl.user_session.set("history", [])
    cl.user_session.set("bot", bot)

    await cl.Message(content=bot["welcome"]).send()


# === Keyword-Based Agent Scoring ===
_KEYWORD_SCORES: Dict[str, Dict[str, float]] = {
    "tta": {"trend": 1.0, "future": 1.0, "absurd": 1.5, "presentism": 1.0, "disruption": 0.8},
    "jtbd": {"customer": 1.0, "job": 1.0, "hire": 1.2, "progress": 0.8, "interview": 0.6, "validation": 0.8},
    "scurve": {"s-curve": 1.5, "technology": 0.8, "adoption": 1.0, "dominant design": 1.2, "lifecycle": 0.8},
    "redteam": {"challenge": 1.0, "assumption": 1.2, "stress test": 1.2, "weakness": 0.8, "devil": 1.0, "debate": 0.8, "pivot": 0.6},
    "larry": {"think": 0.5, "problem": 0.5, "framework": 0.5},
}


def suggest_agents_from_context(
    recent_text: str, current_bot_id: str
) -> list:
    """
    Suggest 2-3 bots ranked by combined keyword + graph score.
    Advisory only — never suppresses the current bot.
    Returns list of (bot_id, final_score, trace) sorted descending.
    """
    text_lower = recent_text.lower()

    # Keyword scoring
    keyword_scores: Dict[str, float] = {}
    for bot_id, keywords in _KEYWORD_SCORES.items():
        for kw, weight in keywords.items():
            if kw in text_lower:
                keyword_scores[bot_id] = keyword_scores.get(bot_id, 0) + weight

    # Graph scoring (additive, never overrides)
    graph_scores, graph_trace = graph_score_agents(recent_text, current_bot_id)

    # Problem-language bonus
    problem_scores: Dict[str, float] = {}
    problem_trace: Dict = {}
    if has_problem_language(recent_text):
        problem_scores, problem_trace = classify_and_route(recent_text, current_bot_id)

    # Merge: final_score = keyword_score + (graph_score * 1.5)
    all_bots = set(keyword_scores) | set(graph_scores) | set(problem_scores)
    merged = []
    for bot_id in all_bots:
        if bot_id == current_bot_id:
            continue  # Never suggest the current bot
        kw = keyword_scores.get(bot_id, 0)
        gs = graph_scores.get(bot_id, 0)
        ps = problem_scores.get(bot_id, 0)
        final = kw + ((gs + ps) * 1.5)
        if final > 0.3:
            merged.append((bot_id, round(final, 2)))

    merged.sort(key=lambda x: x[1], reverse=True)

    # Trace for logging (Constraint 2)
    trace = {
        "query": recent_text[:120],
        "keyword_scores": keyword_scores,
        "graph_trace": graph_trace,
        "problem_trace": problem_trace,
        "final_ranked": [(b, s) for b, s in merged[:3]],
    }
    logger.info(f"graph_route_trace: {trace}")

    return merged[:3]


@cl.on_message
async def main(message: cl.Message):
    """Handle user messages with streaming."""

    bot = cl.user_session.get("bot", BOTS["larry"])
    history = cl.user_session.get("history", [])
    chat_profile = cl.user_session.get("chat_profile") or "larry"
    turn_count = len(history) // 2

    # Graph-enriched context for the active bot
    context_hint = enrich_for_bot(message.content, turn_count, bot_id=chat_profile)
    if context_hint:
        logger.info(context_hint)

    # Build contents for Gemini
    contents = []
    for msg in history:
        contents.append(types.Content(
            role=msg["role"],
            parts=[types.Part(text=msg["content"])]
        ))

    # Optionally prepend graph context as invisible system-level hint
    user_text = message.content
    if context_hint:
        user_text = f"{context_hint}\n\n{message.content}"

    contents.append(types.Content(
        role="user",
        parts=[types.Part(text=user_text)]
    ))

    # Create streaming message
    msg = cl.Message(content="")
    await msg.send()

    try:
        response_stream = client.models.generate_content_stream(
            model="gemini-3-flash-preview",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=bot["system_prompt"],
            ),
        )

        full_response = ""
        for chunk in response_stream:
            if chunk.text:
                full_response += chunk.text
                await msg.stream_token(chunk.text)

        await msg.update()

        # Update history (store original message, not enriched)
        history.append({"role": "user", "content": message.content})
        history.append({"role": "model", "content": full_response})
        cl.user_session.set("history", history)

        # Suggest other bots (advisory, after response)
        if turn_count >= 1:
            suggestions = suggest_agents_from_context(message.content, chat_profile)
            if suggestions:
                actions = []
                for bot_id, score in suggestions:
                    b = BOTS.get(bot_id)
                    if b:
                        actions.append(
                            cl.Action(
                                name="switch_bot",
                                payload={"bot_id": bot_id},
                                label=f"{b['icon']} Try {b['name']}",
                            )
                        )
                if actions:
                    await cl.Message(
                        content="💡 **Based on your conversation, you might also explore:**",
                        actions=actions,
                    ).send()

    except Exception as e:
        await msg.stream_token(f"\n\n⚠️ Error: {str(e)}")
        await msg.update()
