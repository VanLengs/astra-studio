# Astra Studio

A **Claude Code plugin marketplace** for planning, designing, validating, and shipping plugins.

Astra Studio handles the **outer loop** of plugin development — multi-role brainstorming, domain modeling, plugin validation, and promotion. Individual skill authoring and testing is handled by the official [`skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator).

## Plugins

| Plugin | What it does | Install |
|--------|-------------|---------|
| **studio-core** | Workspace management — init, promote, status | `claude plugin install studio-core@astra-studio` |
| **studio-planner** | Plugin planning — event storming, domain modeling, skill design | `claude plugin install studio-planner@astra-studio` |
| **studio-quality** | Quality assurance — plugin validation, MCP wiring | `claude plugin install studio-quality@astra-studio` |

## Quick Start

```bash
# 1. Register the marketplace
claude plugin marketplace add github:VanLengs/astra-studio-plugins

# 2. Install what you need
claude plugin install studio-core@astra-studio
claude plugin install studio-planner@astra-studio
claude plugin install studio-quality@astra-studio

# 3. Initialize studio in your project
/studio-core:init

# 4. Plan a plugin
/studio-planner:plan "your business domain"

# 5. Build each skill (uses official skill-creator)
/skill-creator
# → point it at studio/changes/{plugin}/skills/{skill}/SKILL.md

# 6. Validate the plugin
/studio-quality:validate studio/changes/{plugin}

# 7. Ship it
/studio-core:promote {plugin-name}
```

## Planning Pipeline

`/studio-planner:plan` chains 4 skills with user checkpoints between each:

```
Step 1: event-storm
  Multi-role brainstorming (PM, architect, domain experts)
  → Discovers events, user journeys, pain points, process flows
  → Writes: studio/changes/{domain}/event-storm.md

        ↓ user confirms

Step 2: domain-model
  Clusters events into business domains, draws plugin boundaries
  → Classifies: core vs supporting vs generic
  → Writes: studio/changes/{domain}/domain-map.md

        ↓ user confirms

Step 3: skill-design
  Breaks each plugin into skills with interfaces and data flow
  → Assesses complexity: prompt-only / scripts / MCP
  → Writes: studio/changes/{plugin}/skill-map.md

        ↓ user confirms

Step 4: spec-generate
  Auto-generates all specification files
  → brief.md, plugin.json.draft, SKILL.md skeletons, commands
  → Advances status: planning → building
```

### Subagent Roles

The planning process uses multiple perspectives via subagent roles:

| Role | Perspective | Defined in |
|------|------------|------------|
| **Product Manager** | User personas, journey mapping, pain point prioritization | `agents/product-manager.md` |
| **Architect** | System boundaries, dependencies, technical feasibility | `agents/architect.md` |
| **Domain Expert** | Domain-specific knowledge, real-world constraints | `agents/_domain-expert-template.md` |

Domain experts are **dynamically instantiated** based on the user's business context. For example, a children's health project might get "Children's Nutrition Expert" and "Pediatric Exercise Specialist".

## Full Workflow

```
/studio-core:init                       /studio-planner:plan
        ↓                                       ↓
    studio/                             event-storm.md
    ├── config.yaml                     domain-map.md
    ├── changes/                        skill-map.md
    └── archive/                               ↓
                                        /spec-generate
                                               ↓
                                studio/changes/{plugin}/
                                ├── brief.md
                                ├── plugin.json.draft
                                ├── skill-map.md
                                ├── status.json (building)
                                ├── skills/
                                │   ├── skill-a/SKILL.md  ← skeleton
                                │   └── skill-b/SKILL.md  ← skeleton
                                └── commands/
                                               ↓
                                    /skill-creator (official)
                                               ↓
                                studio/changes/{plugin}/skills/{skill}/
                                ├── SKILL.md        ← fleshed out
                                ├── evals/
                                └── scripts/
                                               ↓
                              /studio-quality:validate
                                               ↓
                                  status → approved
                                               ↓
                              /studio-core:promote
                                               ↓
                              plugins/{collection}/{plugin}/  (shipped)
                              studio/archive/{date}-{plugin}/ (archived)
```

## Architecture

Astra Studio is a **marketplace** (collection of plugins), not a monolithic plugin. Each plugin is independently installable:

- **studio-core**: Zero dependencies. Manages the `studio/` workspace.
- **studio-planner**: Depends on studio-core. Multi-role planning and design.
- **studio-quality**: Zero dependencies. Can validate any plugin, not just studio-managed ones.

The `studio/` directory is **git-tracked** — it holds development documentation (briefs, design decisions, status) with version control value. Inspired by [OpenSpec](https://github.com/Fission-AI/OpenSpec)'s spec-driven workspace pattern.

## Development

```bash
# Test locally
claude --plugin-dir ./studio-core --plugin-dir ./studio-planner --plugin-dir ./studio-quality
```

## License

Apache-2.0
