---
name: platform-docs
description: Generate complete platform documentation suite — chains all 6 generation skills to produce brainmap, agent mapping, tech designs, project plan, visualization, and speech script.
argument-hint: "[domain-name] [--output dir] [--steps all|brainmap|mapping|tech|plan|visual|speech] [--reference path/to/ref.pen]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
---

# Platform Documentation Generator

Generate a complete documentation suite for an industry AI model platform.

## Usage

```
/studio-platform:platform-docs {domain-name}
/studio-platform:platform-docs {domain-name} --steps brainmap,mapping
/studio-platform:platform-docs {domain-name} --output ./platform-docs/
/studio-platform:platform-docs {domain-name} --reference /path/to/reference.pen
```

## Arguments

- `domain-name`: The domain workspace name in `studio/changes/` (required)
- `--output`: Output directory (default: `docs/`)
- `--steps`: Comma-separated list of steps to run (default: `all`)
  - `brainmap` — Step 1: Generate brainmap-index.md + module docs
  - `mapping` — Step 2: Generate agent-plugin-mapping.md
  - `tech` — Step 3: Generate 5 tech design documents
  - `plan` — Step 4: Generate project-plan.md
  - `visual` — Step 5: Generate .pen visualization
  - `speech` — Step 6: Generate presentation speech script
- `--reference`: Path to a reference .pen file for visual generation

## Pipeline

This command orchestrates the full platform documentation pipeline:

```
Step 1: generate-brainmap
  ├── brainmap-index.md
  └── brainmap-module-1~N.md
         ↓
Step 2: generate-agent-mapping
  └── agent-plugin-mapping.md
         ↓
Step 3: generate-tech-designs  (parallelized)
  ├── data-warehouse-design.md
  ├── data-collection-design.md
  ├── knowledge-graph-design.md
  ├── ml-models-design.md
  └── rag-system-design.md
         ↓
Step 4: generate-project-plan
  └── project-plan.md
         ↓
Step 5: generate-platform-visual
  └── {platform-name}.pen
         ↓
Step 6: generate-speech
  └── 迎检话术-{platform-name}.md
```

## Execution Strategy

### Pre-checks
1. Verify `studio/changes/{domain-name}/` exists with `event-storm.md` and `domain-map.md`
2. Verify at least one plugin workspace exists in `studio/changes/` with `skill-map.md`
3. Create output directory if it doesn't exist

### Parallelization
Steps 1-2 are sequential (Step 2 depends on Step 1's output).
Step 3 generates 5 documents — split into 2 parallel agents:
  - Agent A: data-warehouse + data-collection (data layer)
  - Agent B: knowledge-graph + ml-models + rag-system (AI layer)
Step 4 depends on Steps 1-3.
Steps 5-6 depend on all previous steps.

### User Confirmation
After each major step, briefly report what was generated and ask to continue.
On `--steps all` with no interaction, run the full pipeline without pausing.

### Error Recovery
If a step fails:
- Report the error with details
- Offer to retry or skip
- Previously generated files are preserved

## Invokes Skills
1. `generate-brainmap` — Step 1
2. `generate-agent-mapping` — Step 2
3. `generate-tech-designs` — Step 3
4. `generate-project-plan` — Step 4
5. `generate-platform-visual` — Step 5
6. `generate-speech` — Step 6

## Output Summary
On completion, print a summary table:

```
📦 Platform Documentation Suite — {platform_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
| File                          | Size   | Status |
|-------------------------------|--------|--------|
| brainmap-index.md             | XX KB  | ✅     |
| brainmap-module-1~N.md        | XX KB  | ✅     |
| agent-plugin-mapping.md       | XX KB  | ✅     |
| data-warehouse-design.md      | XX KB  | ✅     |
| data-collection-design.md     | XX KB  | ✅     |
| knowledge-graph-design.md     | XX KB  | ✅     |
| ml-models-design.md           | XX KB  | ✅     |
| rag-system-design.md          | XX KB  | ✅     |
| project-plan.md               | XX KB  | ✅     |
| {platform-name}.pen           | XX KB  | ✅     |
| 迎检话术-{platform-name}.md    | XX KB  | ✅     |
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: {N} files, {total_size}
```
