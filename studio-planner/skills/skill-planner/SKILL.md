---
name: skill-planner
description: Design the skill breakdown for a plugin. Use when you have a plugin definition and need to enumerate individual skills, define scope boundaries, map dependencies, and assess complexity. Produces skill skeletons in studio/changes/ that the official skill-creator can flesh out.
allowed-tools: Read, Write, Glob, Grep
user-invocable: true
---

# Skill Planner

Break a plugin down into individual skills with clear scope boundaries, dependency mapping, and complexity assessment.

Consult the decomposition guide at `${CLAUDE_SKILL_DIR}/../../references/skill-decomposition-guide.md` for split/merge rules, naming conventions, complexity tiers, and skeleton format.

## Pre-check

Verify `studio/` exists. If not, tell the user to run `/studio-core:init` first.

## Workflow

1. **Parse input** — read `studio/changes/{name}/plugin.json.draft` or user description
2. **Enumerate skills** — list all skills the plugin needs
3. **Define scope** — inputs, outputs, and boundaries per skill
4. **Map dependencies** — which skills depend on others
5. **Assess complexity** — classify each skill's implementation tier
6. **Write skeletons** — create SKILL.md stubs in `studio/changes/{name}/skills/`

## Step 1: Parse Input

Accept one of:
- A plugin name with a workspace in `studio/changes/{name}/`
- A plugin name + description from the user

If the workspace exists, read `plugin.json.draft` for the plugin's description and skill list, and `brief.md` for business context. Use these to inform skill design.

If existing SKILL.md skeletons are already present in `studio/changes/{name}/skills/`, read them. This skill can refine existing skeletons, not just create from scratch.

## Step 2: Enumerate Skills

List every skill the plugin needs. Apply single responsibility — each skill should do one thing well.

Signs a skill should be split:
- The description uses "and" to join unrelated tasks
- It has more than 3 distinct input types
- Different users would invoke different parts of it

Signs skills should be merged:
- One skill's only purpose is feeding data to another
- They always run in sequence with no user decision point between them

**Naming**: kebab-case, verb-noun pattern preferred (e.g., `analyze-portfolio`, `generate-report`).

## Step 3: Define Scope

For each skill, specify:

| Skill | Inputs | Outputs | Out of scope |
|-------|--------|---------|-------------|
| `analyze-data` | CSV file | Statistics JSON | Visualization |
| `render-chart` | Statistics JSON | PNG chart | Data analysis |

## Step 4: Map Dependencies

Identify which skills depend on others:

```
analyze-data → render-chart → generate-report
                                    ↑
validate-config ────────────────────┘
```

Rules:
- No circular dependencies
- Dependencies should flow in one direction (pipeline pattern)
- Independent skills can run in parallel

## Step 5: Assess Complexity

Classify each skill into an implementation tier:

| Tier | Characteristics | Structure |
|------|-----------------|-----------|
| **Simple** | Prompt-only, no scripts | SKILL.md + references/ |
| **Moderate** | Needs helper scripts | SKILL.md + scripts/ + references/ |
| **Complex** | Multi-stage orchestration | SKILL.md + scripts/ + agents/ |

This tells the official `skill-creator` how much infrastructure to design.

## Step 6: Write Skeletons

For each skill, create a SKILL.md skeleton in the workspace:

```
studio/changes/{plugin-name}/skills/{skill-name}/SKILL.md
```

Skeleton format — compatible with official skill-creator's "existing draft" mode:

```markdown
---
name: {skill-name}
description: {one-line description — make it slightly "pushy" for better triggering}
allowed-tools: {based on complexity tier}
user-invocable: true
---

# {Skill Name}

{2-3 sentence summary of what this skill does}

## Intent
- {What should this skill enable Claude to do?}
- {When should this skill trigger?}

## Expected Inputs
- {What data the skill receives}

## Expected Outputs
- {What the skill produces}

## Workflow
1. {High-level step 1}
2. {High-level step 2}
3. {High-level step 3}
```

Update `status.json` — add each skill with status `draft`.

After this, tell the user: "Skeletons are ready. Use `/skill-creator` to flesh out each skill with full instructions, scripts, and evals."
