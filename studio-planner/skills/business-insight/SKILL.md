---
name: business-insight
description: Analyze a business domain to surface plugin opportunities. Use when a user describes their work, team, or pain points and wants to know what plugins could help. Produces a prioritized list of plugin candidates with rationale and estimated scope, saved to studio/changes/.
allowed-tools: Read, Write, Glob
user-invocable: true
---

# Business Insight

Analyze a business scenario and identify where AI agent plugins could add value. Output is a structured report with pain points, plugin candidates, and priority ranking.

## Pre-check

Verify `studio/` exists. If not, tell the user to run `/studio-core:init` first.

## Workflow

1. **Interview** — understand the domain, users, and workflows
2. **Map pain points** — categorize and score severity
3. **Generate candidates** — propose plugins that address grouped pain points
4. **Prioritize** — rank by impact and feasibility
5. **Produce artifact** — write output to `studio/changes/`

## Step 1: Interview

Gather context about the user's domain. Extract from the conversation first, then ask to fill gaps:

1. **Domain**: What industry or function? (e.g., fintech trading, content marketing, legal compliance)
2. **Persona**: Who are the primary users? What's their technical level?
3. **Current tools**: What do they use today? Where do tools fall short?
4. **Daily workflows**: What takes the most time? What's error-prone?
5. **Success criteria**: What would "10x better" look like?

Keep the interview conversational — adapt questions based on answers. Stop when you have enough context to identify 3-5 pain points.

## Step 2: Map Pain Points

For each pain point:
- **ID**: `PP-1`, `PP-2`, etc.
- **Description**: One sentence describing the problem
- **Category**: Efficiency, Accuracy, Compliance, Integration, or Knowledge
- **Severity**: High (daily impact, significant time/cost), Medium (weekly impact), Low (occasional friction)
- **Current workaround**: How the user handles it today

Present the pain point inventory to the user for validation before proceeding.

## Step 3: Generate Plugin Candidates

Group related pain points into plugin candidates. Each candidate should:
- Address 1-3 pain points (focused scope)
- Have a clear, descriptive name (kebab-case)
- Be implementable as 2-5 skills

For each candidate:
- **ID**: `PC-1`, `PC-2`, etc.
- **Name**: Suggested plugin name
- **Pain points addressed**: List of PP-IDs
- **Rationale**: Why this grouping makes sense
- **Estimated skills**: Number of skills needed
- **Complexity**: Simple (prompt-only), Moderate (scripts needed), Complex (orchestrator-level)

## Step 4: Prioritize

Score each candidate on two axes:
- **Impact**: How much value does it deliver? (1-5)
- **Feasibility**: How easy is it to build? (1-5)

Priority = Impact x Feasibility. Rank candidates by priority score.

Present the ranked list to the user. They may adjust priorities based on factors you can't see.

## Step 5: Produce Artifact

For the top-priority plugin candidate, create the workspace:

```
studio/changes/{plugin-name}/
├── brief.md          # business context, pain points, success criteria
└── status.json       # { plugin, target_collection, phase: "planning", skills: {} }
```

Write `brief.md` with:
- Business context from the interview
- Pain points addressed
- Plugin candidates and priority ranking
- Success criteria

Write `status.json`:
```json
{
  "plugin": "{plugin-name}",
  "target_collection": "plugins",
  "phase": "planning",
  "created_at": "{ISO-8601}",
  "skills": {}
}
```

The next skill in the pipeline (`plugin-planner`) consumes this workspace.
