# OpenSpec Guide — Spec-Driven Development

## Overview

OpenSpec is a spec-driven development framework. It maintains two folder trees:
- `openspec/specs/` — current truth (what IS built)
- `openspec/changes/` — proposals (what SHOULD change)

## Three-Stage Workflow

1. **Proposal** — draft a change with requirements and scenarios
2. **Apply** — implement the code following tasks.md
3. **Archive** — move completed changes, update specs

## Directory Structure

```
openspec/
├── project.md
├── specs/{capability}/
│   ├── spec.md
│   └── design.md
└── changes/{change-id}/
    ├── proposal.md
    ├── tasks.md
    ├── design.md (optional)
    └── specs/{capability}/spec.md
```

## Change ID Naming

Kebab-case, verb-led: `add-sidebar-nav`, `update-task-list`, `remove-legacy-api`

## Proposal.md

```markdown
## Why
[1-2 sentences on problem/opportunity]

## What Changes
- [Bullet list]
- [Mark breaking changes with **BREAKING**]

## Impact
- Affected specs: [capabilities]
- Affected code: [files/systems]
```

## Tasks.md

```markdown
## 1. Implementation
- [ ] 1.1 Create component
- [ ] 1.2 Add routing
- [ ] 1.3 Write tests
```

## Spec Delta Format

```markdown
## ADDED Requirements
### Requirement: Feature Name
The system SHALL provide [capability].

#### Scenario: Success case
- **WHEN** [condition]
- **THEN** [expected result]

## MODIFIED Requirements
### Requirement: Existing Feature
[Complete modified requirement text]

#### Scenario: Updated behavior
- **WHEN** [condition]
- **THEN** [new result]

## REMOVED Requirements
### Requirement: Old Feature
**Reason**: [Why]
**Migration**: [How]
```

## Critical Rules

1. Every requirement MUST have at least one `#### Scenario:` (4 hashtags)
2. Use `SHALL`/`MUST` for normative requirements
3. MODIFIED must include **complete** updated text
4. Scenario format: `#### Scenario: Name` only

## Design.md (Optional)

Create when: cross-cutting change, new dependency, security/performance concerns.

```markdown
## Context
## Goals / Non-Goals
## Decisions
## Risks / Trade-offs
```

## Multi-Capability Changes

Create separate delta files per capability:

```
changes/add-sidebar-nav/specs/
├── navigation/spec.md
└── layout/spec.md
```
