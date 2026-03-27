---
name: status
description: Show the current state of all plugin development in studio/changes/. Use to check what's in progress, what's ready for review, or what needs attention. Also shows recently archived plugins.
allowed-tools: Read, Glob, Grep
user-invocable: true
---

# Studio Status

Display a dashboard of all active plugin development and recent archives.

## Steps

### Step 1: Check studio/ exists

If `studio/` doesn't exist, suggest running `/studio-core:init`.

### Step 2: Scan active changes

For each directory in `studio/changes/` (excluding `.gitkeep`):
1. Read `status.json` — if missing, show the plugin with phase "unknown"
2. Extract: plugin name, phase, target_collection, skill statuses
3. Calculate completion: count skills with status `tested` or `approved` vs total skill count

If `studio/changes/` is empty (only `.gitkeep`), note "No active plugins" and skip to Step 3.

### Step 3: Scan recent archives

List the 5 most recent directories in `studio/archive/` by name (date-prefixed).
For each, read `status.json` to get `shipped_to` path if available.

If `studio/archive/` is empty, note "No shipped plugins yet".

### Step 4: Display dashboard

Format as a table:

```
Studio Status
═════════════

Active (studio/changes/)
┌──────────────────┬────────────┬────────────────┬───────────┐
│ Plugin           │ Phase      │ Skills         │ Target    │
├──────────────────┼────────────┼────────────────┼───────────┤
│ deal-flow        │ building   │ 1/3 tested     │ plugins/  │
│ risk-monitor     │ approved   │ 2/2 tested     │ plugins/  │
└──────────────────┴────────────┴────────────────┴───────────┘

Recently Shipped (studio/archive/)
  2026-03-25-auth-plugin → plugins/my-collection/auth-plugin
  2026-03-20-data-tools  → plugins/data-tools
```

### Step 5: Suggest next actions

Based on current state, suggest what to do next:
- If a plugin is `approved`: "Run `/studio-core:promote {name}` to ship it"
- If a plugin is `building`: "Use `/skill-creator` to build individual skills"
- If a plugin is `planning`: "Continue with `/studio-planner:plan`"
- If no active changes: "Run `/studio-planner:plan <domain>` to start"
