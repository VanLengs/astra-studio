---
name: event-storm
description: Run a multi-role brainstorming session to discover business events, user journeys, pain points, and processes. Use when starting a new plugin project, exploring a business domain, or when someone says "let's brainstorm" or "help me figure out what to build". Produces a structured event storm with personas, journeys, and process flows.
allowed-tools: Read, Write, Glob, Agent
user-invocable: true
---

# Event Storm

Run a structured brainstorming session with multiple perspectives — product manager, architect, and domain experts — to discover what's really going on in a business domain and where plugins can help.

## Pre-check

1. Verify `studio/` exists. If not, run the init skill first.
2. Read `${CLAUDE_SKILL_DIR}/../../agents/product-manager.md` — this defines the PM perspective.
3. Read `${CLAUDE_SKILL_DIR}/../../agents/architect.md` — this defines the architect perspective.
4. Read `${CLAUDE_SKILL_DIR}/../../agents/_domain-expert-template.md` — this is the template for domain experts.

## Workflow

1. **Set the stage** — understand the domain and assemble roles
2. **Discover events** — what happens in the business?
3. **Map user journeys** — walk through real user workflows
4. **Identify hotspots** — where are the pain points and opportunities?
5. **Model processes** — organize events into time-ordered flows
6. **Write output** — save event storm results to studio/changes/

## Step 1: Set the Stage

Ask the user to describe their business domain in 2-3 sentences. Extract:
- **Industry/function**: What field is this? (e.g., pediatric health, fintech, content marketing)
- **Target users**: Who will use the plugins being designed?
- **Current situation**: What tools/processes exist today?

Based on the domain, **propose 2-4 domain expert roles**. Fill in the template from `_domain-expert-template.md` with concrete titles and descriptions. Examples:

| Domain | Suggested experts |
|--------|------------------|
| Children's health | Children's Nutrition Expert, Pediatric Exercise Specialist |
| Financial services | Portfolio Risk Analyst, Compliance Officer |
| Content marketing | SEO Strategist, Content Operations Manager |

Present the proposed roles to the user. They can adjust, add, or remove roles. Once confirmed, the brainstorming begins.

## Step 2: Discover Events

Adopt each role in turn and contribute **business events** — things that happen in the domain. For each event:

- **What happened**: past tense, one sentence (e.g., "Child's weekly meal plan was generated")
- **Who triggered it**: which actor or system
- **What it affects**: downstream consequences

Use the Agent tool to run each role as a subagent. Give each subagent:
- The role definition (from agents/*.md)
- The domain context from Step 1
- The instruction: "List 5-10 business events from your perspective"

Collect all events and **deduplicate** — different roles may describe the same event differently. Present the combined event list to the user for validation.

## Step 3: Map User Journeys

Have the **product manager** role lead this step. For each user persona identified:

1. **Persona card**: Name, role, goal, context, technical level
2. **Journey steps**: What the user does, step by step, from trigger to outcome
3. **Pain points per step**: Where they struggle, get frustrated, or make mistakes
4. **Emotional arc**: Where are they confident vs confused vs anxious?

Use the Agent tool with the product-manager.md role definition. Give it:
- The events discovered in Step 2
- The instruction: "Map the user journey for each persona, marking pain points at each step"

Present journey maps to the user. Ask: "Does this match your experience? What's missing?"

## Step 4: Identify Hotspots

Synthesize events and journeys to find **hotspots** — areas with concentrated pain, high frequency, or high stakes.

For each hotspot:
- **ID**: `HS-1`, `HS-2`, etc.
- **Description**: What's going wrong or could be better
- **Evidence**: Which events and journey pain points point here
- **Severity**: High (daily impact, significant cost) / Medium (weekly friction) / Low (occasional annoyance)
- **Type**: Efficiency (too slow), Accuracy (error-prone), Knowledge (hard to find info), Integration (tools don't talk), Compliance (regulatory risk)

Rank hotspots by severity. Present to the user: "These are the biggest opportunities. Do you agree with the ranking?"

## Step 5: Model Processes

Organize the events into **time-ordered process flows**. For each major process:

1. **Trigger**: What starts this process?
2. **Steps**: Events in sequence, with actors
3. **Decision points**: Where does someone need to make a choice? (Mark with ◇)
4. **Parallel branches**: What can happen simultaneously?
5. **End state**: What's the successful outcome?

Format as a text flow diagram:

```
[Trigger] → Event A → Event B → ◇ Decision
                                    ├→ Path 1 → Event C → [Done]
                                    └→ Path 2 → Event D → Event E → [Done]
```

Decision points and parallel branches are **natural boundaries for skill splitting** — note this for the next skill (domain-model).

## Step 6: Write Output

Create the workspace and save results:

```
studio/changes/{domain-slug}/
├── event-storm.md       # full brainstorming output
└── status.json          # { phase: "planning" }
```

**Derive `{domain-slug}`** from the domain description: lowercase, kebab-case, 2-3 words (e.g., "children-health", "trading-ops").

Write `event-storm.md` with the following sections:

```markdown
# Event Storm: {Domain}

> Date: {YYYY-MM-DD}
> Roles: {list of roles used}

## Domain Context
{Summary from Step 1}

## Personas
{Persona cards from Step 3}

## User Journeys
{Journey maps from Step 3}

## Events
{Categorized event list from Step 2}

## Hotspots
{Ranked hotspot list from Step 4}

## Process Flows
{Flow diagrams from Step 5}

## Decision Points
{List of all ◇ decision points — these inform skill boundaries}
```

Write `status.json` — this is a **domain-level** workspace (not yet a plugin). The `type` field distinguishes it:

```json
{
  "type": "domain",
  "domain": "{domain-slug}",
  "phase": "planning",
  "created_at": "{ISO-8601}",
  "plugins": []
}
```

Note: domain-level workspaces have `"type": "domain"` and a `plugins` list (initially empty). Plugin-level workspaces have `"type": "plugin"` and a `skills` map. The `domain-model` skill will create plugin-level workspaces and populate the `plugins` list here.

Tell the user: "Event storm complete. Run `/studio-planner:domain-model {domain-slug}` to identify plugin boundaries, or run `/studio-planner:plan {domain-slug}` to continue the full pipeline."
