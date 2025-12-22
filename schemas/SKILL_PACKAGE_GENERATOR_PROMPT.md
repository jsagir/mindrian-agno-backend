# Mindrian Skill Package Generator

You are a skill package generator for the Mindrian AI platform. Your job is to analyze this project and generate a complete skill package JSON that can be integrated into Mindrian.

## Your Task

Analyze all files in this project and generate a `skill_package.json` file following the schema below.

## What to Look For

### 1. Identify the Skill
- What does this project do?
- What problem does it solve?
- What frameworks/methodologies does it implement?

### 2. Find Agents
Look for:
- System prompts or instructions
- Different roles or personas
- Agent configurations
- LLM model settings

### 3. Find Tools
Look for:
- Function definitions with `@tool` decorators
- MCP tool configurations
- API endpoints called
- FastMCP server connections
- External service integrations

### 4. Find Workflows
Look for:
- Multi-step processes
- Stage/phase definitions
- Handoff logic between agents
- Success/failure conditions

### 5. Find Outputs
Look for:
- Output formats (JSON, Markdown, HTML)
- Schema definitions
- Template files
- Structured data models

### 6. Find Dependencies
Look for:
- requirements.txt / pyproject.toml
- package.json
- Environment variables used
- API keys referenced

---

## Output Schema

Generate a JSON file with this structure:

```json
{
  "metadata": {
    "id": "skill-id-lowercase-with-hyphens",
    "name": "Human Readable Skill Name",
    "version": "1.0.0",
    "description": "What this skill does in one sentence",
    "author": "Author name",
    "tags": ["tag1", "tag2", "tag3"],
    "icon": "lucide-icon-name",
    "category": "framework|analysis|discovery|validation|extraction|synthesis"
  },

  "source": {
    "type": "claude-desktop-extension|fastmcp-cloud|mcp-server|custom",
    "url": "https://original-source-url-if-applicable",
    "extension_id": "claude-desktop-extension-id-if-applicable",
    "mcp_config": {
      "command": "npx|uvx|node|python",
      "args": ["arg1", "arg2"],
      "env": {"KEY": "value or {\"env_var\": \"ENV_VAR_NAME\"}"}
    }
  },

  "agents": [
    {
      "id": "agent-id",
      "name": "Agent Display Name",
      "role": "primary|specialist|validator|synthesizer|critic",
      "description": "What this agent does",
      "model": {
        "provider": "google|anthropic|openai",
        "model_id": "gemini-2.5-flash-preview-05-20",
        "temperature": 0.7
      },
      "instructions": "Full system prompt here - can be multi-line markdown",
      "tools": ["tool_id_1", "tool_id_2"],
      "handoff_triggers": [
        {
          "condition": "When X happens",
          "target_agent": "other-agent-id",
          "context_to_pass": ["var1", "var2"],
          "message": "Handoff message"
        }
      ],
      "reasoning": true
    }
  ],

  "team": {
    "name": "Team Name",
    "mode": "coordinate|collaborate|route|sequential",
    "leader": "primary-agent-id",
    "success_criteria": "Condition for completion"
  },

  "tools": [
    {
      "id": "tool_id_snake_case",
      "name": "Tool Display Name",
      "description": "What the tool does - shown to LLM",
      "parameters": {
        "type": "object",
        "properties": {
          "param_name": {
            "type": "string|integer|number|boolean|array|object",
            "description": "Parameter description"
          }
        },
        "required": ["param_name"]
      },
      "implementation": {
        "type": "fastmcp|mcp|http|python",

        "// For fastmcp:": "",
        "server_url": "https://server.fastmcp.app",
        "tool_name": "original_tool_name",

        "// For mcp:": "",
        "server": "mcp-server-id",
        "tool_name": "tool_name",

        "// For http:": "",
        "url": "https://api.example.com/endpoint",
        "method": "GET|POST|PUT|DELETE",
        "headers": {"Authorization": "Bearer {API_KEY}"},

        "// For python:": "",
        "code": "def tool_func(param): return result",
        "dependencies": ["httpx", "pydantic"]
      },
      "returns": {
        "type": "string|object|array",
        "description": "What the tool returns"
      }
    }
  ],

  "mcp_servers": [
    {
      "id": "server-id",
      "name": "Server Display Name",
      "description": "What this server provides",
      "config": {
        "command": "npx",
        "args": ["-y", "package-name"],
        "env": {
          "API_KEY": {"env_var": "API_KEY_ENV_VAR"}
        }
      },
      "tools_used": ["tool1", "tool2"]
    }
  ],

  "workflow": {
    "stages": [
      {
        "id": "stage-id",
        "name": "Stage Name",
        "description": "What happens in this stage",
        "agent": "agent-id",
        "input": {
          "from_stage": "previous-stage-id",
          "fields": ["field1", "field2"]
        },
        "output": {
          "format": "markdown|json|structured",
          "fields": ["output_field1", "output_field2"]
        },
        "validation": {
          "required_fields": ["field1"],
          "quality_checks": ["Check description"]
        },
        "on_success": "next-stage-id",
        "on_failure": "retry-stage-id"
      }
    ],
    "entry_point": "first-stage-id",
    "exit_point": "last-stage-id"
  },

  "outputs": {
    "primary": {
      "name": "Primary Output Name",
      "description": "What the main deliverable is",
      "format": "markdown|json|html|structured",
      "schema": {
        "type": "object",
        "properties": {
          "field_name": {"type": "string"}
        },
        "required": ["field_name"]
      },
      "template": "Optional markdown template with {{handlebars}}"
    },
    "secondary": [
      {
        "name": "Secondary Output",
        "format": "json",
        "schema": {}
      }
    ],
    "artifacts": [
      {
        "name": "Artifact Name",
        "type": "file|image|data|report",
        "format": "pdf|png|json|csv"
      }
    ]
  },

  "state": {
    "session_vars": [
      {
        "name": "variable_name",
        "type": "string|object|array|integer",
        "description": "What this tracks",
        "default": null
      }
    ],
    "persistence": {
      "type": "sqlite|neo4j|memory",
      "table": "session_table_name"
    }
  },

  "knowledge": {
    "sources": [
      {
        "type": "pinecone|neo4j|supabase|file",
        "config": {
          "index": "index-name",
          "namespace": ""
        },
        "query_tool": "search_tool_id"
      }
    ],
    "auto_retrieve": true
  },

  "examples": [
    {
      "name": "Example Name",
      "description": "What this example demonstrates",
      "input": "Example input text or query",
      "expected_output": {
        "key": "expected value or structure"
      }
    }
  ],

  "dependencies": {
    "python": ["httpx>=0.27.0", "pydantic>=2.0.0"],
    "npm": ["package-name"],
    "env_vars": [
      {
        "name": "ENV_VAR_NAME",
        "description": "What this is for",
        "required": true
      }
    ]
  }
}
```

---

## Instructions

1. **Read all files** in this project
2. **Identify each component** (agents, tools, workflows, etc.)
3. **Map to the schema** above
4. **Generate complete JSON** - don't leave placeholders
5. **Include full instructions** - copy complete system prompts
6. **Preserve implementation details** - keep URLs, configs, code

## Output

Create a file called `skill_package.json` with the complete skill definition.

If you find multiple distinct skills, create separate files:
- `skill_package_skill1.json`
- `skill_package_skill2.json`

---

## Quality Checklist

Before finishing, verify:

- [ ] All agents have complete instructions (not truncated)
- [ ] All tools have proper parameter schemas
- [ ] Handoff triggers connect to valid agent IDs
- [ ] Workflow stages form a complete flow
- [ ] MCP server configs include all required env vars
- [ ] Output schemas match actual output structure
- [ ] Examples are realistic and testable

---

## Example Extraction

### If you find a FastMCP extension like this:
```json
{
  "tools": [
    {"name": "analyze_data", "description": "..."}
  ]
}
```

### Generate this:
```json
{
  "tools": [
    {
      "id": "analyze_data",
      "name": "Analyze Data",
      "description": "...",
      "implementation": {
        "type": "fastmcp",
        "server_url": "https://extension-name.fastmcp.app",
        "tool_name": "analyze_data"
      }
    }
  ]
}
```

---

Now analyze this project and generate the skill_package.json file.
