---
description: Plan a new plugin — analyze domain, design architecture, decompose into skills
argument-hint: [business domain or plugin idea]
---

Plan a complete plugin from scratch by chaining three skills in sequence:

1. **business-insight** — Analyze the domain described by `$ARGUMENTS`, interview the user about pain points, and produce a prioritized list of plugin candidates. Write output to `studio/changes/{slug}/brief.md`.

2. **plugin-planner** — Design the plugin architecture: collection structure, core vs add-on roles, manifest drafts. Write `plugin.json.draft` to the workspace.

3. **skill-planner** — Decompose each plugin into individual skills with scope, dependencies, and complexity. Create SKILL.md skeletons in `studio/changes/{slug}/skills/`.

Before starting, verify `studio/` exists. If not, run the init skill first.

After planning is complete, suggest: "Use `/skill-creator` to flesh out each skill skeleton with full instructions, scripts, and evals."
