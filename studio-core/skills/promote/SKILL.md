---
name: promote
description: Finalize and ship an approved plugin — convert the manifest draft to production, archive design documents, and mark the plugin as shipped. Use when a plugin has passed validation, all skills are tested, and you want to ship it.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
user-invocable: true
---

# Studio Promote

Finalize a completed plugin for production and archive the design workspace. Implementation files already live in the target plugin directory (written there by `spec-generate` and developed in place) — promote only needs to finalize the manifest and archive the design docs.

## Design Principle

`studio/changes/` holds **design documents** (brief.md, skill-map.md, plugin.json.draft, status.json). Implementation files (SKILL.md, commands, scripts, hooks) live directly in the **target plugin directory** as the single source of truth. Promote does NOT copy implementation files — they are already where they belong.

Promote works identically for `action: "create"` and `action: "modify"` — in both cases it finalizes the manifest and archives the change workspace.

## Pre-conditions

1. If `$ARGUMENTS` is empty, scan `studio/changes/` for plugins with phase `approved` and list them. If exactly one, use it. If multiple, ask the user to choose. If none, explain what's needed and exit.
2. Read `studio/changes/$ARGUMENTS/status.json`
3. Verify `phase` is `approved` — if not, show the current phase and explain:
   - `planning` → "Run `/studio-planner:plan` to complete the design"
   - `building` → "Use `/skill-creator` to finish building skills"
   - `testing` → "Run `/studio-quality:validate` to approve it"
   - `shipped` → "This plugin has already been shipped"
4. Read `target_dir` from status.json (fallback: derive from `target_collection` + plugin name)
5. Verify `{target_dir}/` exists and contains at least a `skills/` directory with SKILL.md files
6. Verify all skills in status.json have status `tested` or `approved`

If pre-conditions fail, print a clear message about what needs to happen first and exit.

## Promote Steps

### Step 1: Verify target plugin directory

Check that `{target_dir}/` already has the expected structure:

```
{target_dir}/
├── skills/
│   └── {skill-name}/
│       └── SKILL.md         # should already exist (written by spec-generate, developed by skill-creator)
├── commands/                # should already exist if skills are user-invocable
└── ...                      # scripts/, hooks/, .mcp.json may also exist
```

If the target directory is missing or empty, abort: "Target directory `{target_dir}/` does not contain implementation files. Did you run `/studio-planner:spec-generate` first?"

### Step 2: Finalize plugin manifest

Read `studio/changes/{name}/plugin.json.draft` and write the production manifest to `{target_dir}/.claude-plugin/plugin.json`:

- Remove the `.draft` suffix
- Ensure `name`, `version`, `description` are present
- Set `skills` to `"./skills/"`
- Add `"commands": "./commands/"` if a commands/ directory exists in the target
- Add `"hooks": "./hooks/hooks.json"` if a hooks/ directory exists in the target
- Add `"mcpServers": "./.mcp.json"` if a .mcp.json file exists in the target

### Step 3: Archive design workspace

Move `studio/changes/{name}/` to `studio/archive/{YYYY-MM-DD}-{name}/`

Update the archived `status.json`:
- Set `phase` to `shipped`
- Add `shipped_at` timestamp
- Add `shipped_to` path (the `target_dir` value)

### Step 4: Report

Print:
- What was promoted and where: "Plugin `{name}` finalized at `{target_dir}/`"
- Manifest location: `{target_dir}/.claude-plugin/plugin.json`
- Archive location: `studio/archive/{date}-{name}/`
- Remind user to review and commit: "Review the finalized plugin, then commit when ready"

## Does NOT

- Copy implementation files — they already live in `{target_dir}/`
- Run `git add` or `git commit` — the user decides when to commit
- Delete implementation files — only design docs are archived
- Run validation — that should have happened before approval
