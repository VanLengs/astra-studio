# Astra Studio

A **Claude Code plugin marketplace** for planning, designing, validating, and shipping plugins.

Astra Studio handles the **outer loop** of plugin development — business analysis, architecture design, plugin validation, and promotion. Individual skill authoring and testing is handled by the official [`skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator).

## Plugins

| Plugin | What it does | Install |
|--------|-------------|---------|
| **studio-core** | Workspace management — init, promote, status | `claude plugin install studio-core@astra-studio` |
| **studio-planner** | Plugin planning — business insight, architecture, skill decomposition | `claude plugin install studio-planner@astra-studio` |
| **studio-quality** | Quality assurance — plugin validation, MCP wiring | `claude plugin install studio-quality@astra-studio` |

## Quick Start

```bash
# 1. Register the marketplace
claude plugin marketplace add github:VanLengs/astra-studio

# 2. Install what you need
claude plugin install studio-core@astra-studio
claude plugin install studio-planner@astra-studio
claude plugin install studio-quality@astra-studio

# 3. Initialize studio in your project
/studio-core:init

# 4. Plan a plugin
/studio-planner:plan "your business domain or plugin idea"

# 5. Build each skill (uses official skill-creator)
/skill-creator
# → point it at studio/changes/{plugin}/skills/{skill}/SKILL.md

# 6. Validate the plugin
/studio-quality:validate studio/changes/{plugin}

# 7. Ship it
/studio-core:promote {plugin-name}
```

## How It Works

```
/studio-planner:plan                    /skill-creator (official)
        ↓                                       ↓
studio/changes/{plugin}/               studio/changes/{plugin}/skills/{skill}/
├── brief.md                           ├── SKILL.md        ← fleshed out
├── plugin.json.draft                  ├── evals/
├── status.json                        │   ├── evals.json
└── skills/                            │   └── results.json
    ├── skill-a/SKILL.md  ← skeleton  ├── scripts/
    └── skill-b/SKILL.md  ← skeleton  └── references/
        ↓                                       ↓
/studio-quality:validate               /studio-core:promote
        ↓                                       ↓
   status → approved                plugins/{collection}/{plugin}/  (shipped)
                                    studio/archive/{date}-{plugin}/ (archived)
```

## Architecture

Astra Studio is a **marketplace** (collection of plugins), not a monolithic plugin. Each plugin is independently installable:

- **studio-core**: Zero dependencies. Manages the `studio/` workspace.
- **studio-planner**: Depends on studio-core. Handles analysis and design.
- **studio-quality**: Zero dependencies. Can validate any plugin, not just studio-managed ones.

The `studio/` directory is **git-tracked** — it holds development documentation (briefs, design decisions, status) with version control value. Inspired by [OpenSpec](https://github.com/Fission-AI/OpenSpec)'s spec-driven workspace pattern.

## Development

```bash
# Test locally
claude --plugin-dir ./studio-core --plugin-dir ./studio-planner --plugin-dir ./studio-quality
```

## License

Apache-2.0
