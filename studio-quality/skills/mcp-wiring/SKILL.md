---
name: mcp-wiring
description: Configure MCP server connections for a plugin. Use when a plugin needs external tool access, you want to generate or update a .mcp.json file, wire up filesystem access, database connections, API integrations, or troubleshoot MCP server configuration.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
user-invocable: true
---

# MCP Wiring

Configure MCP (Model Context Protocol) server connections for a plugin by scanning skill requirements, matching to available servers, and generating a validated `.mcp.json` file.

## Workflow

1. **Identify plugin** — get the plugin directory path
2. **Scan requirements** — detect what MCP tools the skills need
3. **Match servers** — map requirements to available MCP server packages
4. **Generate config** — produce `.mcp.json` with correct entries
5. **Validate** — verify the generated config is well-formed
6. **Review with user** — confirm server choices and env var requirements

## Step 1: Identify Plugin

Accept the plugin directory path. The `.mcp.json` file will be created/updated at the plugin root, alongside `.claude-plugin/plugin.json`.

If the plugin already has a `.mcp.json`, read it first — merge new entries rather than overwriting.

## Step 2: Scan Requirements

Scan all SKILL.md files in the plugin and detect:
- `allowed-tools` frontmatter entries referencing MCP tools (e.g., `mcp__server__tool`)
- Tool references in body text suggesting external capabilities
- Explicit MCP mentions in instructions

## Step 3: Match Servers

Map each requirement to a known MCP server:

| Requirement | MCP Server | Package |
|------------|------------|---------|
| Filesystem access | `@anthropic/mcp-filesystem` | `npx -y @anthropic/mcp-filesystem <path>` |
| Web search | `@anthropic/mcp-web-search` | `npx -y @anthropic/mcp-web-search` |
| GitHub access | `@modelcontextprotocol/server-github` | `npx -y @modelcontextprotocol/server-github` |
| Database (PostgreSQL) | `@modelcontextprotocol/server-postgres` | `npx -y @modelcontextprotocol/server-postgres` |
| Slack | `@modelcontextprotocol/server-slack` | `npx -y @modelcontextprotocol/server-slack` |

For the latest catalog, search the MCP registry if available:
```
Use tool: mcp__mcp-registry__search_mcp_registry
```

If a requirement has no known server match, flag it for the user.

## Step 4: Generate Config

Generate `.mcp.json` with the standard structure:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@package/name", "..."],
      "env": {
        "KEY": "${ENV_VAR}"
      }
    }
  }
}
```

Use `${CLAUDE_PLUGIN_ROOT}` for plugin-relative paths.
Use `${CLAUDE_PLUGIN_DATA}` for persistent data paths.

## Step 5: Validate

Check:
- `.mcp.json` is valid JSON
- Each server entry has `command` field
- Environment variables are documented
- No duplicate server names
- Plugin manifest references `.mcp.json` (`"mcpServers": "./.mcp.json"`)

## Step 6: Review with User

Present the generated config:
1. List each MCP server and what it provides
2. Highlight environment variables that need to be set
3. Note any unmatched requirements
4. Confirm the user wants to write the config

After approval, update the plugin manifest to reference `.mcp.json` if not already declared.
