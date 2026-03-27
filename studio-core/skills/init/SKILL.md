---
name: init
description: Initialize a plugin development studio in the current project. Use when starting plugin development in a new repo, when someone says "set up studio", or when studio/ directory is missing. Creates a git-tracked workspace for planning, building, and shipping plugins.
allowed-tools: Read, Write, Bash, Glob
user-invocable: true
---

# Studio Init

Initialize `studio/` directory in the current project for plugin development. This directory is git-tracked — it holds development documentation (briefs, drafts, status) that has version control value.

Inspired by [OpenSpec](https://github.com/Fission-AI/OpenSpec)'s `openspec init` pattern: a spec-driven workspace initialized into the project repo.

## Pre-check

1. Check if `studio/` already exists at the project root
   - If yes: read `studio/config.yaml`, report current status, list active changes, and exit
   - If no: proceed with initialization

## Steps

1. Create the directory structure:

```
studio/
├── config.yaml          # studio configuration
├── changes/             # active plugin development (one dir per plugin)
│   └── .gitkeep
└── archive/             # completed and archived plugin dev records
    └── .gitkeep
```

2. Write `studio/config.yaml` from the template at `${CLAUDE_SKILL_DIR}/../../templates/config.yaml`
3. Print a summary of what was created
4. Suggest next steps:
   - "Run `/studio-planner:plan <domain>` to start planning your first plugin"
   - "Or create a plugin workspace manually: `mkdir studio/changes/my-plugin`"

## Notes

- `studio/` is meant to be committed to git — it contains development decisions and rationale
- `studio/changes/` holds active work; `studio/archive/` holds shipped work
- Each plugin gets its own directory under `changes/` with brief.md, status.json, and skill drafts
- The official `skill-creator` skill handles individual skill authoring and eval — studio handles the plugin-level orchestration around it
