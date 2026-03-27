#!/usr/bin/env python3
"""Generate .mcp.json for a plugin based on scan results.

Usage:
    python generate_mcp_json.py <plugin-dir> [--merge]

Reads scan results (from scan_mcp_requirements.py output or stdin),
generates a .mcp.json file, and optionally merges with existing config.
"""

import json
import sys
from pathlib import Path


def generate_mcp_config(scan_result: dict, existing: dict | None = None) -> dict:
    """Generate .mcp.json from scan results, optionally merging with existing."""
    config = {"mcpServers": {}}

    # Start with existing config if merging
    if existing:
        config["mcpServers"] = dict(existing.get("mcpServers", {}))

    # Add matched servers from scan
    for server_name, info in scan_result.get("matched_servers", {}).items():
        if server_name not in config["mcpServers"]:
            entry = {
                "command": info["command"],
                "args": list(info["args"]),
            }

            # Add common env vars based on server type
            env = get_default_env(server_name)
            if env:
                entry["env"] = env

            config["mcpServers"][server_name] = entry

    return config


def get_default_env(server_name: str) -> dict:
    """Return default environment variables for known server types."""
    env_map = {
        "github": {"GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"},
        "slack": {"SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}"},
        "brave-search": {"BRAVE_API_KEY": "${BRAVE_API_KEY}"},
        "postgres": {"POSTGRES_CONNECTION_STRING": "${DATABASE_URL}"},
    }
    return env_map.get(server_name, {})


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_mcp_json.py <plugin-dir> [--merge]", file=sys.stderr)
        sys.exit(1)

    plugin_dir = sys.argv[1]
    merge = "--merge" in sys.argv
    root = Path(plugin_dir).resolve()

    if not root.is_dir():
        print(f"Error: '{plugin_dir}' is not a directory", file=sys.stderr)
        sys.exit(1)

    # Read scan results from stdin
    try:
        scan_result = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print("Error: Could not parse scan results from stdin", file=sys.stderr)
        print("Pipe the output of scan_mcp_requirements.py into this script", file=sys.stderr)
        sys.exit(1)

    # Load existing .mcp.json if merging
    existing = None
    mcp_path = root / ".mcp.json"
    if merge and mcp_path.exists():
        try:
            existing = json.loads(mcp_path.read_text())
        except json.JSONDecodeError:
            print(f"Warning: Existing .mcp.json is invalid, starting fresh", file=sys.stderr)

    # Generate config
    config = generate_mcp_config(scan_result, existing)

    if not config["mcpServers"]:
        print("No MCP servers needed — no .mcp.json generated")
        print(json.dumps({"generated": False, "reason": "no servers matched"}, indent=2))
        return

    # Write .mcp.json
    mcp_path.write_text(json.dumps(config, indent=2) + "\n")

    output = {
        "generated": True,
        "path": str(mcp_path),
        "servers": list(config["mcpServers"].keys()),
        "config": config,
    }
    print(json.dumps(output, indent=2))

    # Report env vars that need to be set
    env_vars = set()
    for server in config["mcpServers"].values():
        for val in server.get("env", {}).values():
            if "${" in val:
                env_vars.add(val.strip("${}"))

    if env_vars:
        print(f"\nEnvironment variables to configure: {', '.join(sorted(env_vars))}", file=sys.stderr)


if __name__ == "__main__":
    main()
