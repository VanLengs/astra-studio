---
description: Plan a new plugin — brainstorm, model domains, design skills, generate specs
argument-hint: [business domain or plugin idea]
---

Plan a complete plugin from scratch by chaining four skills in sequence:

1. **event-storm** — Run a multi-role brainstorming session for the domain described by `$ARGUMENTS`. Discover business events, user journeys, pain points, and process flows. Saves results to `studio/changes/{slug}/event-storm.md`.

2. **domain-model** — Analyze the event storm output to identify business domains, draw plugin boundaries, and classify core vs supporting vs generic capabilities. Saves domain map to `studio/changes/{slug}/domain-map.md`.

3. **skill-design** — Break each plugin into individual skills with clear responsibilities, data flow, and complexity assessment. Saves skill map to `studio/changes/{slug}/skill-map.md`.

4. **spec-generate** — Automatically generate all specification files: brief.md, plugin.json.draft, SKILL.md skeletons, and commands. Advances status from `planning` to `building`.

Before starting, verify `studio/` exists. If not, run the init skill first.

After each step, pause and present results to the user for validation before proceeding to the next step. The user may want to adjust findings at any point.

After planning is complete, suggest: "Use `/skill-creator` to flesh out each skill skeleton with full instructions, scripts, and evals."
