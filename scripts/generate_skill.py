#!/usr/bin/env python3
"""
Skill Package Generator

Transforms a skill package JSON into Mindrian-compatible Python code.

Usage:
    python scripts/generate_skill.py path/to/skill_package.json

Generates:
    - agents/{skill_id}.py - Agent definitions
    - tools/{skill_id}_tools.py - Tool implementations
    - teams/{skill_id}_team.py - Team configuration
    - workflows/{skill_id}_workflow.py - Workflow definition
"""

import json
import os
import sys
from pathlib import Path
from typing import Any


def load_skill_package(path: str) -> dict:
    """Load and validate skill package JSON."""
    with open(path) as f:
        return json.load(f)


def generate_agent_code(agent: dict, skill_id: str) -> str:
    """Generate Python code for an agent."""
    tools_list = ", ".join(agent.get("tools", []))

    # Generate handoff triggers as comments/documentation
    handoff_docs = ""
    if agent.get("handoff_triggers"):
        handoff_docs = "\n# Handoff Triggers:\n"
        for trigger in agent["handoff_triggers"]:
            handoff_docs += f"#   - {trigger['condition']} -> {trigger['target_agent']}\n"

    return f'''
{agent["id"].replace("-", "_")} = Agent(
    name="{agent["name"]}",
    id="{agent["id"]}",
    model=get_gemini_model(),
    instructions=["""{agent["instructions"]}"""],
    tools=[{tools_list}],
    markdown=True,
    db=mindrian_db,
    description="{agent.get("description", "")}",
    reasoning={agent.get("reasoning", True)},
    stream_intermediate_steps=True,
){handoff_docs}
'''


def generate_tool_code(tool: dict) -> str:
    """Generate Python code for a tool."""
    impl = tool["implementation"]
    params = tool.get("parameters", {}).get("properties", {})
    required = tool.get("parameters", {}).get("required", [])

    # Generate parameter signature
    param_parts = []
    for name, config in params.items():
        param_type = config.get("type", "str")
        type_map = {"string": "str", "integer": "int", "number": "float", "boolean": "bool", "array": "list", "object": "dict"}
        py_type = type_map.get(param_type, "Any")

        if name in required:
            param_parts.append(f"{name}: {py_type}")
        else:
            default = config.get("default", "None")
            if isinstance(default, str) and py_type == "str":
                default = f'"{default}"'
            param_parts.append(f"{name}: {py_type} = {default}")

    params_sig = ", ".join(param_parts) if param_parts else ""

    # Generate implementation based on type
    if impl["type"] == "fastmcp":
        impl_code = f'''    result = call_fastmcp_tool(
        "{impl["server_url"]}",
        "{impl["tool_name"]}",
        {{{", ".join(f'"{p}": {p}' for p in params.keys())}}}
    )
    return str(result)'''
    elif impl["type"] == "mcp":
        impl_code = f'''    # Call MCP server: {impl["server"]}
    # Tool: {impl["tool_name"]}
    raise NotImplementedError("MCP tool call - implement via MCP client")'''
    elif impl["type"] == "http":
        impl_code = f'''    response = httpx.{impl["method"].lower()}("{impl["url"]}", json={{...}})
    return response.json()'''
    elif impl["type"] == "python":
        impl_code = impl.get("code", "    pass")
    else:
        impl_code = "    pass"

    return f'''
@tool
def {tool["id"]}({params_sig}) -> str:
    """
    {tool["description"]}
    """
{impl_code}
'''


def generate_team_code(skill: dict) -> str:
    """Generate team configuration code."""
    team_config = skill.get("team", {})
    agents = skill.get("agents", [])

    member_ids = [a["id"].replace("-", "_") for a in agents]
    members_str = ", ".join(member_ids)

    return f'''
{skill["metadata"]["id"].replace("-", "_")}_team = Team(
    name="{team_config.get("name", skill["metadata"]["name"] + " Team")}",
    description="{skill["metadata"]["description"]}",
    model=Gemini(id="gemini-3-flash-preview", api_key=os.getenv("GOOGLE_AI_API_KEY")),
    members=[{members_str}],
    instructions=["""
{team_config.get("instructions", "")}

## Success Criteria
{team_config.get("success_criteria", "Task completed successfully")}
"""],
    markdown=True,
)
'''


def generate_workflow_code(skill: dict) -> str:
    """Generate workflow definition code."""
    workflow = skill.get("workflow", {})
    if not workflow:
        return ""

    stages = workflow.get("stages", [])

    stages_code = []
    for stage in stages:
        stages_code.append(f'''    Step(
        id="{stage["id"]}",
        name="{stage["name"]}",
        agent={stage["agent"].replace("-", "_")},
        # {stage.get("description", "")}
    )''')

    return f'''
{skill["metadata"]["id"].replace("-", "_")}_workflow = Workflow(
    name="{skill["metadata"]["name"]} Workflow",
    steps=[
{chr(10).join(stages_code)}
    ],
)
'''


def generate_agents_file(skill: dict) -> str:
    """Generate complete agents file."""
    skill_id = skill["metadata"]["id"]
    skill_name = skill["metadata"]["name"]

    # Collect tool imports
    tool_ids = set()
    for agent in skill.get("agents", []):
        tool_ids.update(agent.get("tools", []))

    tools_import = ", ".join(sorted(tool_ids))

    # Generate agent code
    agents_code = []
    for agent in skill.get("agents", []):
        agents_code.append(generate_agent_code(agent, skill_id))

    # Generate registry
    agent_ids = [a["id"].replace("-", "_") for a in skill.get("agents", [])]
    registry_entries = ",\n    ".join(f'"{a["id"]}": {a["id"].replace("-", "_")}' for a in skill.get("agents", []))

    # Generate agent list for list_agents function
    agent_list = []
    for a in skill.get("agents", []):
        agent_list.append({
            "id": a["id"],
            "name": a["name"],
            "role": a.get("role", "primary"),
            "description": a.get("description", "")
        })
    agent_list_str = json.dumps(agent_list, indent=8)

    return f'''"""
{skill_name} Agents

Auto-generated from skill package: {skill_id}
Version: {skill["metadata"]["version"]}

{skill["metadata"]["description"]}
"""

import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.db.sqlite import AsyncSqliteDb

from tools.{skill_id.replace("-", "_")}_tools import (
    {tools_import}
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
        id="gemini-3-flash-preview",
        api_key=os.getenv("GOOGLE_AI_API_KEY"),
    )


# Shared database
mindrian_db = AsyncSqliteDb(db_file="mindrian.db", session_table="{skill_id.replace("-", "_")}_sessions")


# =============================================================================
# AGENTS
# =============================================================================
{chr(10).join(agents_code)}

# =============================================================================
# REGISTRY
# =============================================================================

{skill_id.replace("-", "_").upper()}_AGENTS = {{
    {registry_entries}
}}


def get_{skill_id.replace("-", "_")}_agent(agent_id: str) -> Agent:
    """Get an agent by ID."""
    return {skill_id.replace("-", "_").upper()}_AGENTS.get(agent_id)


def list_{skill_id.replace("-", "_")}_agents() -> list[dict]:
    """List all agents in this skill."""
    return {agent_list_str}
'''


def generate_tools_file(skill: dict) -> str:
    """Generate complete tools file."""
    skill_id = skill["metadata"]["id"]
    skill_name = skill["metadata"]["name"]

    tools = skill.get("tools", [])

    # Check if we need fastmcp helper
    has_fastmcp = any(t["implementation"]["type"] == "fastmcp" for t in tools)

    fastmcp_helper = '''
def call_fastmcp_tool(server_url: str, tool_name: str, arguments: dict) -> dict:
    """Call a FastMCP cloud tool via HTTP."""
    try:
        response = httpx.post(
            f"{server_url}/tools/{tool_name}",
            json={"arguments": arguments},
            timeout=120.0,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

''' if has_fastmcp else ''

    # Generate tool code
    tools_code = []
    for tool in tools:
        tools_code.append(generate_tool_code(tool))

    # Generate exports
    tool_ids = [t["id"] for t in tools]
    exports = ", ".join(tool_ids)

    return f'''"""
{skill_name} Tools

Auto-generated from skill package: {skill_id}
Version: {skill["metadata"]["version"]}
"""

import os
import httpx
from agno.tools import tool
from typing import Any, Optional


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
{fastmcp_helper}

# =============================================================================
# TOOLS
# =============================================================================
{chr(10).join(tools_code)}

# =============================================================================
# EXPORTS
# =============================================================================

{skill_id.replace("-", "_").upper()}_TOOLS = [{exports}]
'''


def generate_team_file(skill: dict) -> str:
    """Generate complete team file."""
    skill_id = skill["metadata"]["id"]
    skill_name = skill["metadata"]["name"]

    # Agent imports
    agent_imports = ", ".join(a["id"].replace("-", "_") for a in skill.get("agents", []))

    team_code = generate_team_code(skill)

    return f'''"""
{skill_name} Team

Auto-generated from skill package: {skill_id}
Version: {skill["metadata"]["version"]}
"""

import os
from agno.team import Team
from agno.models.google import Gemini

from agents.{skill_id.replace("-", "_")} import (
    {agent_imports}
)


# =============================================================================
# TEAM CONFIGURATION
# =============================================================================
{team_code}
'''


def generate_output_schema(skill: dict) -> str:
    """Generate Pydantic models for outputs."""
    outputs = skill.get("outputs", {})
    primary = outputs.get("primary", {})

    if not primary.get("schema"):
        return ""

    schema = primary["schema"]

    # Generate Pydantic model
    fields = []
    for name, config in schema.get("properties", {}).items():
        py_type = {
            "string": "str",
            "integer": "int",
            "number": "float",
            "boolean": "bool",
            "array": "list",
            "object": "dict"
        }.get(config.get("type", "string"), "Any")

        if name in schema.get("required", []):
            fields.append(f"    {name}: {py_type}")
        else:
            fields.append(f"    {name}: Optional[{py_type}] = None")

    return f'''
from pydantic import BaseModel
from typing import Optional, Any, List


class {skill["metadata"]["id"].replace("-", "_").title().replace("_", "")}Output(BaseModel):
    """{primary.get("description", primary["name"])} output model."""
{chr(10).join(fields)}
'''


def generate_skill_package(skill_path: str, output_dir: str = None):
    """Generate all files from a skill package."""
    skill = load_skill_package(skill_path)
    skill_id = skill["metadata"]["id"]

    if output_dir is None:
        output_dir = Path(__file__).parent.parent
    else:
        output_dir = Path(output_dir)

    # Create directories if needed
    (output_dir / "agents").mkdir(exist_ok=True)
    (output_dir / "tools").mkdir(exist_ok=True)
    (output_dir / "teams").mkdir(exist_ok=True)

    # Generate files
    files_generated = []

    # Tools file
    tools_file = output_dir / "tools" / f"{skill_id.replace('-', '_')}_tools.py"
    tools_file.write_text(generate_tools_file(skill))
    files_generated.append(str(tools_file))

    # Agents file
    agents_file = output_dir / "agents" / f"{skill_id.replace('-', '_')}.py"
    agents_file.write_text(generate_agents_file(skill))
    files_generated.append(str(agents_file))

    # Team file
    team_file = output_dir / "teams" / f"{skill_id.replace('-', '_')}_team.py"
    team_file.write_text(generate_team_file(skill))
    files_generated.append(str(team_file))

    print(f"Generated skill package: {skill['metadata']['name']}")
    print(f"Files created:")
    for f in files_generated:
        print(f"  - {f}")

    return files_generated


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_skill.py <skill_package.json> [output_dir]")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    generate_skill_package(skill_path, output_dir)
