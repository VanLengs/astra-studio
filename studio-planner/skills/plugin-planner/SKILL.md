---
name: plugin-planner
description: Design plugin collection architecture from business insight or user requirements. Use when you need to plan how many plugins to create, define core vs add-on boundaries, draft manifests, and establish skill allocation across plugins. Reads from studio/changes/ and updates the workspace.
allowed-tools: Read, Write, Glob, Grep
user-invocable: true
---

# Plugin Planner

Design the architecture of a plugin collection — how many plugins, their roles, boundaries, and skill allocation.

## Pre-check

Verify `studio/` exists. If not, tell the user to run `/studio-core:init` first.

## Workflow

1. **Parse input** — read `studio/changes/{name}/brief.md` or user description
2. **Design collection** — decide collection name and plugin boundaries
3. **Assign roles** — core vs add-on for each plugin
4. **Draft manifests** — create plugin.json.draft per plugin
5. **Map skills** — allocate skills to plugins
6. **Update workspace** — write artifacts to `studio/changes/`

## Step 1: Parse Input

Accept one of:
- A plugin name that has a workspace in `studio/changes/{name}/brief.md`
- A freeform description of what the user wants to build

If reading a brief, extract pain points and plugin candidates as the starting point.

## Step 2: Design Collection

A **collection** is a namespace that groups related plugins (also a marketplace repo):

| Scenario | Collection strategy |
|----------|-------------------|
| 1 plugin candidate | Single plugin, no collection overhead |
| 2-3 related candidates | One collection with core + add-on(s) |
| 4+ candidates or distinct domains | Multiple collections with clear boundaries |

**Collection naming**: kebab-case, short, descriptive (e.g., `trading-ops`, `content-studio`).

## Step 3: Assign Roles

Each plugin gets a role:

| Role | Criteria | Example |
|------|----------|---------|
| **core** | Other plugins depend on it. Removing it breaks the collection. | `trading-core` |
| **add-on** | Optional enhancement. Can be disabled independently. | `trading-signals` |

Rules:
- At most one `core` plugin per collection
- A collection can be all `add-on` if plugins are independent

## Step 4: Draft Manifests

For each plugin, draft a `plugin.json` following the Claude Code plugin spec:

```json
{
  "name": "plugin-name",
  "version": "0.1.0",
  "description": "What this plugin does",
  "author": { "name": "Team Name" },
  "license": "Apache-2.0",
  "keywords": ["relevant", "keywords"],
  "skills": "./skills/",
  "commands": "./commands/"
}
```

No `x-astra` extensions — keep it standard Claude Code compatible.

## Step 5: Map Skills

Allocate skills to plugins based on:
- **Cohesion**: Skills that share data/context go in the same plugin
- **Independence**: Skills that can function alone are add-on candidates
- **Reuse**: Shared utilities belong in the core plugin

For each plugin, list skill names, one-line descriptions, and dependencies.

## Step 6: Update Workspace

If this is a single-plugin scenario, update the existing workspace:

```
studio/changes/{plugin-name}/
├── brief.md              # already exists
├── plugin.json.draft     # ← write this
├── status.json           # ← update phase to "planning", add skills
└── skills/               # ← create skeleton dirs
    ├── skill-a/
    │   └── SKILL.md      # skeleton with name + description only
    └── skill-b/
        └── SKILL.md
```

If this is a multi-plugin collection, create a workspace per plugin.

Update `status.json`:
```json
{
  "plugin": "{name}",
  "target_collection": "plugins",
  "phase": "planning",
  "created_at": "...",
  "skills": {
    "skill-a": "draft",
    "skill-b": "draft"
  }
}
```

The next step: use the official `/skill-creator` to flesh out each SKILL.md skeleton.
