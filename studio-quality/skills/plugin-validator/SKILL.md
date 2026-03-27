---
name: plugin-validator
description: Validate a completed plugin for structural correctness, manifest compliance, skill quality, and dependency integrity. Use when a plugin is ready for review, before packaging or promotion, after editing a plugin, or when you want a detailed diagnostic report with remediation steps. Works on any Claude Code plugin directory.
allowed-tools: Bash, Read, Write, Glob, Grep
user-invocable: true
---

# Plugin Validator

Run comprehensive validation on a plugin and produce an actionable report. Checks manifest schema, skill quality, cross-references, and dependency integrity.

## Workflow

1. **Identify plugin** — get the plugin directory path from the user
2. **Structural validation** — manifest and directory checks
3. **Skill validation** — SKILL.md quality checks
4. **Dependency checks** — MCP and inter-skill dependencies
5. **Present findings** — summarize pass/fail with remediation steps
6. **Update studio status** — if the plugin is in `studio/changes/`, update status.json

## Step 1: Identify Plugin

Accept the plugin directory path via `$ARGUMENTS`. The path can be:
- A `studio/changes/{name}/` workspace (development)
- A `plugins/{name}/` directory (production)
- Any directory with `.claude-plugin/plugin.json`

If the user gives a skill directory, navigate up to find the plugin root.

## Step 2: Structural Validation

Check the following and report pass/fail for each:

- [ ] `.claude-plugin/plugin.json` exists and is valid JSON
- [ ] Required fields present: `name`, `version`, `description`
- [ ] Plugin name matches directory name (kebab-case)
- [ ] `name` follows pattern: `^[a-z][a-z0-9-]*$`
- [ ] `version` follows semver: `^\d+\.\d+\.\d+`
- [ ] `skills` path in manifest points to an existing directory
- [ ] `hooks` path resolves if declared
- [ ] `mcpServers` path resolves if declared
- [ ] `commands` path resolves if declared

## Step 3: Skill Validation

For each skill directory found:

- [ ] `SKILL.md` exists
- [ ] YAML frontmatter is valid
- [ ] `name` field present and matches directory name
- [ ] `description` present, under 1024 chars
- [ ] No unexpected frontmatter keys (warn on unknown keys)
- [ ] Line count under 500 (warn if over)
- [ ] Referenced `scripts/*.py` files exist
- [ ] Referenced `references/*.md` files exist

## Step 4: Dependency Checks

- [ ] If `.mcp.json` exists: valid JSON, each server has `command` field
- [ ] Environment variables in MCP config are documented
- [ ] If `hooks` declared: hooks.json is valid, event names are recognized
- [ ] If `dependencies` in manifest: listed plugins exist or are documented

## Step 5: Present Findings

Summarize the report:

```
Plugin Validation: {plugin-name}
══════════════════════════════════

Structure:  ✅ 8/8 passed
Skills:     ⚠️ 3/4 passed (1 warning)
Dependencies: ✅ 2/2 passed

Warnings:
  - skills/data-loader/SKILL.md: 520 lines (recommend < 500)

Overall: PASS (with warnings)
```

Categories:
- **Error**: Must fix before shipping
- **Warning**: Advisory, worth addressing
- **Pass**: All good

## Step 6: Update Studio Status (optional)

If the plugin is in `studio/changes/` and all checks pass:
- Ask the user if they want to update `status.json` phase to `approved`
- If yes, update the file

If checks fail, suggest specific remediation steps for each failure.
