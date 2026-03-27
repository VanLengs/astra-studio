#!/usr/bin/env python3
"""Scan plugin skills for MCP server requirements.

Usage:
    python scan_mcp_requirements.py <plugin-dir>

Scans all SKILL.md files to detect:
    - allowed-tools referencing mcp__* tools
    - Tool references in body text suggesting MCP capabilities
    - Explicit MCP mentions in instructions
"""

import json
import re
import sys
from pathlib import Path


# Known MCP tool patterns and their server mappings
MCP_TOOL_PATTERNS = {
    r"mcp__filesystem": {
        "server": "filesystem",
        "package": "@anthropic/mcp-filesystem",
        "command": "npx",
        "args": ["-y", "@anthropic/mcp-filesystem"],
    },
    r"mcp__web[-_]?search": {
        "server": "web-search",
        "package": "@anthropic/mcp-web-search",
        "command": "npx",
        "args": ["-y", "@anthropic/mcp-web-search"],
    },
    r"mcp__github": {
        "server": "github",
        "package": "@modelcontextprotocol/server-github",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
    },
    r"mcp__postgres": {
        "server": "postgres",
        "package": "@modelcontextprotocol/server-postgres",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-postgres"],
    },
    r"mcp__slack": {
        "server": "slack",
        "package": "@modelcontextprotocol/server-slack",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-slack"],
    },
    r"mcp__puppeteer": {
        "server": "puppeteer",
        "package": "@modelcontextprotocol/server-puppeteer",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-puppeteer"],
    },
    r"mcp__brave[-_]?search": {
        "server": "brave-search",
        "package": "@modelcontextprotocol/server-brave-search",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-brave-search"],
    },
}

# Keyword patterns that suggest MCP needs
CAPABILITY_KEYWORDS = {
    "database": "Database access detected — may need an MCP database server",
    "postgresql": "PostgreSQL reference — consider mcp-postgres server",
    "mysql": "MySQL reference — consider an MCP MySQL server",
    "sqlite": "SQLite reference — consider an MCP SQLite server",
    "web search": "Web search reference — consider mcp-web-search server",
    "browser": "Browser reference — consider mcp-puppeteer server",
    "slack": "Slack reference — consider mcp-slack server",
    "github api": "GitHub API reference — consider mcp-github server",
    "filesystem access": "Filesystem access reference — consider mcp-filesystem server",
}


def scan_skill(skill_md: Path) -> dict:
    """Scan a single SKILL.md for MCP requirements."""
    text = skill_md.read_text()
    skill_name = skill_md.parent.name
    findings = {
        "skill": skill_name,
        "mcp_tools": [],
        "capability_hints": [],
        "raw_mcp_refs": [],
    }

    # Check allowed-tools for mcp__ references
    frontmatter_match = re.search(r"allowed-tools:\s*(.+)", text)
    if frontmatter_match:
        tools_line = frontmatter_match.group(1)
        mcp_tools = re.findall(r"mcp__\w+", tools_line)
        findings["mcp_tools"].extend(mcp_tools)

    # Check body for mcp__ tool references
    body_mcp = re.findall(r"mcp__[a-zA-Z0-9_]+__[a-zA-Z0-9_]+", text)
    for ref in body_mcp:
        if ref not in findings["mcp_tools"]:
            findings["raw_mcp_refs"].append(ref)

    # Check for capability keywords
    text_lower = text.lower()
    for keyword, hint in CAPABILITY_KEYWORDS.items():
        if keyword in text_lower:
            findings["capability_hints"].append(hint)

    return findings


def scan_plugin(plugin_dir: str) -> dict:
    """Scan all skills in a plugin for MCP requirements."""
    root = Path(plugin_dir).resolve()
    skills_dir = root / "skills"

    result = {
        "plugin": root.name,
        "skills": [],
        "matched_servers": {},
        "unmatched": [],
    }

    if not skills_dir.is_dir():
        return result

    all_mcp_refs = set()

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        findings = scan_skill(skill_md)
        result["skills"].append(findings)
        all_mcp_refs.update(findings["mcp_tools"])
        all_mcp_refs.update(findings["raw_mcp_refs"])

    # Match references to known servers
    for ref in all_mcp_refs:
        matched = False
        for pattern, server_info in MCP_TOOL_PATTERNS.items():
            if re.search(pattern, ref):
                server_name = server_info["server"]
                if server_name not in result["matched_servers"]:
                    result["matched_servers"][server_name] = {
                        "package": server_info["package"],
                        "command": server_info["command"],
                        "args": server_info["args"],
                        "referenced_by": [],
                    }
                result["matched_servers"][server_name]["referenced_by"].append(ref)
                matched = True
                break
        if not matched:
            result["unmatched"].append(ref)

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python scan_mcp_requirements.py <plugin-dir>", file=sys.stderr)
        sys.exit(1)

    plugin_dir = sys.argv[1]
    if not Path(plugin_dir).is_dir():
        print(f"Error: '{plugin_dir}' is not a directory", file=sys.stderr)
        sys.exit(1)

    result = scan_plugin(plugin_dir)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
