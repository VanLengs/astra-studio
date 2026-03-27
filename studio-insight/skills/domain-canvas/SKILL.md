---
name: domain-canvas
description: Create a domain canvas that maps business domains, their classifications (core/supporting/generic), boundaries, and relationships. Use when you need to understand system architecture, draw service boundaries, decide what to build vs buy, or when someone asks "how should we structure this". Produces a structured domain model document.
allowed-tools: Read, Write, Glob, Grep, Agent
user-invocable: true
---

# Domain Canvas

Produce a domain canvas — a visual map of business domains, their roles, boundaries, and interactions. Helps decide what deserves a custom plugin (core), what's supporting, and what can use off-the-shelf tools.

## Expert Discovery

This skill uses **dynamic expert loading**. On every run:

1. **Primary role**: Always load `architect.md` (leads domain analysis)
2. **Scan project experts**: Glob `studio/agents/*.md` — load all custom experts the team has created
3. **Scan built-in experts**: Glob `${CLAUDE_SKILL_DIR}/../../agents/*.md` — load shipped experts (skip any already loaded from project)
4. **Match by relevance**: From the loaded experts, select those relevant to the current domain context. Match by comparing the expert's `## Your Domain` section and title against the user's input topic. Include 1-3 most relevant domain experts.
5. **Skip template**: Do not load `_domain-expert-template.md` — it's for creating new experts, not for consultation.

The primary role produces the initial artifact. Domain experts review and correct it in the Expert Review step.

## Inputs

Accept one of:
- A domain description via `$ARGUMENTS` (e.g., "儿童健康管理平台")
- A workspace path — read `event-storm.md` for events and `personas/` for actors

## Workflow

1. **Discover domains** — identify distinct business areas
2. **Define boundaries** — what each domain owns and doesn't own
3. **Classify** — core vs supporting vs generic
4. **Map relationships** — how domains interact
5. **Draw canvas** — produce the visual domain map
6. **Expert review** — domain experts verify boundaries and classifications
7. **Validate** — present to user
8. **Write output** — save domain canvas document

## Step 1: Discover Domains

Identify distinct business areas by clustering:
- **By data ownership**: entities that are always accessed together
- **By actor**: who interacts with this area
- **By business rule**: rules that apply to the same concepts
- **By change frequency**: things that change together

Use the **language test**: if practitioners use different vocabulary, it's probably a different domain.

Name each domain in **plain business language** (2-3 words):
- Good: "营养管理", "运动追踪", "健康报告"
- Bad: "NutritionService", "Module3", "后端逻辑"

## Step 2: Define Boundaries

For each domain, specify:

```
┌─────────────────────────────────────┐
│  {Domain Name}                      │
├─────────────────────────────────────┤
│  Owns:                              │
│  - {data entities}                  │
│  - {business rules}                 │
│  - {user-facing capabilities}       │
│                                     │
│  Does NOT own:                      │
│  - {explicit exclusions}            │
│  - {things that belong elsewhere}   │
│                                     │
│  Key actors:                        │
│  - {who interacts with this domain} │
│                                     │
│  Key events:                        │
│  - {events this domain produces}    │
│  - {events this domain consumes}    │
└─────────────────────────────────────┘
```

The boundary test: "If I removed this domain entirely, would the others still make sense?"

## Step 3: Classify

Assess each domain:

```
┌───────────────────────────────────────────────────────────┐
│                    Domain Classification                   │
├──────────────┬──────────┬─────────────────────────────────┤
│ Domain       │ Type     │ Rationale                       │
├──────────────┼──────────┼─────────────────────────────────┤
│ 营养管理      │ Core     │ 核心差异化，用户选择产品的原因      │
│ 运动追踪      │ Support  │ 重要辅助，但不是主打              │
│ 用户档案      │ Generic  │ 标准 CRUD，内置工具可满足          │
│ 健康报告      │ Support  │ 有价值但依赖其他域数据             │
└──────────────┴──────────┴─────────────────────────────────┘
```

| Type | Meaning | Build strategy |
|------|---------|---------------|
| **Core** | Unique value, competitive advantage | Custom plugin, invest in quality |
| **Supporting** | Necessary but not differentiating | Add-on plugin, adequate quality |
| **Generic** | Standard capability | Use existing tools (MCP, built-in) |

## Step 4: Map Relationships

Define how domains interact:

| Relationship | Symbol | Meaning |
|-------------|--------|---------|
| Feeds into | `──▶` | A produces data that B consumes |
| Shares data | `◀──▶` | Both read/write same entities |
| Independent | `· · ·` | No interaction |
| Orchestrates | `══▶` | A coordinates B's behavior |

## Step 5: Draw Canvas

Produce the domain canvas as a visual map:

```
┌──────────────────────────────────────────────────┐
│                Domain Canvas                      │
│                {Project Name}                     │
├──────────────────────────────────────────────────┤
│                                                  │
│   ┌──────────────┐         ┌──────────────┐     │
│   │  营养管理 ★    │──▶──▶──│  健康报告     │     │
│   │  [Core]       │         │  [Supporting] │     │
│   └──────┬───────┘         └──────▲───────┘     │
│          │                        │              │
│          │ shares                  │ feeds        │
│          ▼                        │              │
│   ┌──────────────┐               │              │
│   │  用户档案     │               │              │
│   │  [Generic]   │               │              │
│   └──────┬───────┘               │              │
│          │                        │              │
│          │ feeds                   │              │
│          ▼                        │              │
│   ┌──────────────┐               │              │
│   │  运动追踪     │──▶──▶────────┘              │
│   │  [Supporting] │                              │
│   └──────────────┘                              │
│                                                  │
│  ★ = Core domain                                │
│  [Generic] domains → use existing tools          │
└──────────────────────────────────────────────────┘
```

## Step 6: Expert Review

If domain experts were discovered in Expert Discovery, use the Agent tool to have each relevant expert review the domain canvas.

Give each expert subagent:
- Their agent definition (.md file content)
- The draft domain canvas (domains, boundaries, classifications, relationships)
- The instruction: "Review this domain model from your expertise. Flag: domains that are split wrong (things that belong together are separated, or vice versa), classifications that are wrong (something marked generic that's actually core, or vice versa), relationships that are missing or incorrect, and boundary definitions that don't match how the domain actually works."

Incorporate corrections. Common improvements from domain experts:
- Domains that outsiders lump together but practitioners know are distinct
- Capabilities classified as generic that actually need domain-specific logic
- Relationships that are tighter (or looser) than the architect assumed
- Boundary definitions that use the wrong terminology

If no relevant domain experts were found, skip this step.

## Step 7: Validate

Present the canvas to the user:
- "Does this domain structure match your mental model?"
- "Do you agree with the core/supporting/generic classifications?"
- "Are the relationships correct?"
- "Is anything missing?"

## Step 8: Write Output

If working within a studio workspace:
```
studio/changes/{domain}/domain-canvas.md
```

If standalone, write to the current directory.

The file contains:
- Domain inventory with boundary definitions
- Classification table with rationale
- Relationship map (text diagram)
- Full domain canvas visualization
- Build strategy recommendations (which domains → plugins, which → existing tools)
