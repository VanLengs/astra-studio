---
name: domain-model
description: Analyze event storm results to identify business domains, draw plugin boundaries, and map relationships between them. Use after event-storm, when you have a set of events and processes and need to decide how many plugins to build and what each one owns. Produces a domain map with plugin candidates.
allowed-tools: Read, Write, Glob, Grep, Agent
user-invocable: true
---

# Domain Model

Take the raw output from event-storm and organize it into clear business domains, each mapping to a potential plugin. Determine what's core vs supporting vs off-the-shelf.

Consult `${CLAUDE_SKILL_DIR}/../../references/plugin-architecture-guide.md` for collection architecture patterns and core/add-on decision framework.

## Pre-check

1. Verify `studio/` exists.
2. If `$ARGUMENTS` is provided, read `studio/changes/$ARGUMENTS/event-storm.md`. If it doesn't exist, ask the user to run `/studio-planner:event-storm` first.
3. If no argument, scan `studio/changes/` for workspaces that have `event-storm.md` but no `domain-map.md`. If exactly one, use it. If multiple, ask the user to choose.
4. Read `${CLAUDE_SKILL_DIR}/../../agents/architect.md` — the architect perspective leads this step.

## Workflow

1. **Cluster events** — group related events into business domains
2. **Draw boundaries** — define what each domain owns
3. **Classify domains** — core vs supporting vs generic
4. **Map relationships** — how domains interact
5. **Propose plugins** — translate domains into plugin candidates
6. **Write output** — save domain map to the workspace

## Step 1: Cluster Events

Read the events and process flows from `event-storm.md`. Group them by **business affinity** — events that share the same data, actors, or business rules belong together.

Guidelines for clustering:
- Events that must happen **atomically** (all-or-nothing) belong in the same domain
- Events that different **user personas** own may indicate separate domains
- Events connected by **data flow** often cluster together
- When in doubt, use the **language test**: do practitioners use the same vocabulary for these events? If yes, same domain.

Present the clusters to the user: "I see these natural groupings — does this match how you think about your business?"

## Step 2: Draw Boundaries

For each domain cluster, define:

- **Name**: 2-3 words, plain language (e.g., "Meal Planning", "Exercise Tracking", "Progress Reports")
- **Owns**: What events, data, and decisions belong exclusively to this domain
- **Does NOT own**: What's explicitly out of scope (prevents scope creep)
- **Key actors**: Who interacts with this domain

The boundary test: "If I removed this domain entirely, would the other domains still make sense on their own?" If not, the boundaries are wrong.

## Step 3: Classify Domains

Use the **architect** perspective to classify each domain:

| Classification | Meaning | Plugin strategy |
|---------------|---------|-----------------|
| **Core** | This is the unique value — what makes the product special | Custom plugin, invest heavily in skill quality |
| **Supporting** | Necessary but not differentiating — supports core domains | Add-on plugin, simpler skills, adequate quality |
| **Generic** | Standard capability available everywhere | Use existing tools (MCP servers, built-in Claude features), no custom plugin |

Ask the user to validate classifications: "I think {domain} is your core capability because... Do you agree?"

Generic domains should map to existing solutions:
- Data persistence → MCP filesystem or database server
- Web research → MCP web-search
- GitHub integration → MCP GitHub server
- Communication → MCP Slack server

## Step 4: Map Relationships

Define how the non-generic domains interact:

| Relationship | Meaning | Plugin implication |
|-------------|---------|-------------------|
| **Feeds into** | Domain A produces data that B consumes | B depends on A; consider A as core |
| **Shares data** | Both domains read/write the same data | Shared templates/references, or one owns the data |
| **Independent** | Domains don't interact | Separate plugins, no dependency |
| **Orchestrates** | One domain coordinates multiple others | The orchestrator is likely the core plugin |

Draw the relationship map:

```
[Meal Planning] ──feeds into──→ [Shopping List]
       │                              │
       └──shares data──→ [Nutrition Tracking] ←──independent──→ [Exercise Tracking]
```

## Step 5: Propose Plugins

Translate each non-generic domain into a plugin candidate:

For each candidate:
- **Plugin name**: kebab-case, derived from domain name (e.g., `meal-planner`)
- **Domain**: Which domain it represents
- **Role**: `core` or `add-on` (from classification)
- **Responsibility**: 1-2 sentence description of what it does
- **Expected skills**: Rough list of capabilities (will be refined in skill-design)
- **Dependencies**: Which other plugins it depends on
- **MCP needs**: External services it might need (from generic domain analysis)

Decide the collection structure:
- 1 plugin → single plugin, no collection
- 2-5 related plugins → one collection with clear core
- Independent plugins in different domains → separate collections

Present to the user for validation. This is a key decision point — the user should explicitly approve the plugin structure before proceeding.

## Step 6: Write Output

Write `studio/changes/{name}/domain-map.md`:

```markdown
# Domain Map: {Domain}

> Date: {YYYY-MM-DD}

## Business Domains

### {Domain 1 Name}
- **Classification**: Core / Supporting / Generic
- **Owns**: {events, data, decisions}
- **Does not own**: {explicit exclusions}
- **Actors**: {who interacts}

### {Domain 2 Name}
...

## Relationship Map
{Text diagram from Step 4}

## Plugin Candidates

| Plugin | Domain | Role | Description | Dependencies |
|--------|--------|------|-------------|-------------|
| {name} | {domain} | core | {desc} | — |
| {name} | {domain} | add-on | {desc} | {core-name} |

## Generic Capabilities (no custom plugin needed)
- {capability} → {existing solution}

## Collection Structure
- **Pattern**: {single / core+add-on / independent}
- **Rationale**: {why this structure}
```

For each confirmed plugin candidate, create a **plugin-level** workspace as a peer directory alongside the domain workspace:

```
studio/changes/{plugin-name}/
└── status.json
```

Each plugin's `status.json` references back to the domain workspace:

```json
{
  "type": "plugin",
  "plugin": "{plugin-name}",
  "domain": "{domain-slug}",
  "target_collection": "plugins",
  "phase": "planning",
  "created_at": "{ISO-8601}",
  "skills": {}
}
```

The `domain` field points to `studio/changes/{domain-slug}/` where `event-storm.md` and `domain-map.md` live. This avoids duplicating domain-level artifacts into each plugin workspace.

Also update the domain workspace's `status.json` to register the plugins:

```json
{
  "type": "domain",
  "domain": "{domain-slug}",
  "phase": "planning",
  "created_at": "...",
  "plugins": ["{plugin-name-1}", "{plugin-name-2}"]
}
```

Tell the user: "Domain model complete. Run `/studio-planner:skill-design {plugin-name}` to design skills for each plugin."
