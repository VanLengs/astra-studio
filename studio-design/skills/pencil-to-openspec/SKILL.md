---
name: pencil-to-openspec
description: Convert a Pencil (.pen) prototype file into an OpenSpec change proposal. Use when you have a .pen design prototype and need to generate structured requirements, scenarios, and implementation tasks for the UI. Produces proposal.md, tasks.md, and spec delta files.
allowed-tools: Read, Write, Bash, Glob, Grep
user-invocable: true
---

# Pencil to OpenSpec

Parse a `.pen` prototype file and generate an OpenSpec change proposal that describes the UI requirements, acceptance scenarios, and implementation tasks.

## Pre-conditions

1. **Locate the .pen file**: 
   - If `$ARGUMENTS` specifies a path, use it
   - Otherwise search for `.pen` files in `docs/design/`
   - If multiple found, list them and ask the user to choose
   - If none found, explain that a .pen file is needed and suggest running `screenshot-to-pencil` first

2. **Check for existing OpenSpec workspace**:
   - Look for `openspec/` directory in the project root
   - If it doesn't exist, create it with `openspec/specs/` and `openspec/changes/`
   - If it exists, read `openspec/project.md` for conventions
   - Run `ls openspec/changes/` to check for active changes and avoid conflicts

3. **Load references**: Read `references/openspec-guide.md` and `references/component-mapping.md`

## Analysis Steps

### Step 1: Parse the .pen File

Read and analyze the .pen JSON:

1. **List all frames** (top-level children) with names, dimensions
2. **Extract design tokens** from `variables`
3. **Identify reusable components** (nodes with `reusable: true`)
4. **Build component inventory**: For each frame, catalog:
   - UI components (buttons, inputs, cards, sidebar, etc.)
   - Text content (labels, placeholders, headings)
   - Icons used
   - Layout patterns (flex direction, gaps, alignment)
   - Interactive elements (things that imply user actions)

### Step 2: Map Frames to Capabilities

Group frames into logical capabilities:

**Mapping rules:**
- Frames showing the same page in different states → **single capability** with multiple scenarios
  - Example: "1. New Task (Empty State)", "1a. Dropdown expanded", "1b. Task submitted" → capability `task-creation`
- Frames showing distinct pages → **separate capabilities**
  - Example: "Task List" and "Agent Gallery" → `task-list` and `agent-gallery`
- Reusable components (sidebar, header) → **shared capability** or cross-cutting requirement

**Naming:** Use kebab-case verb-noun format: `task-creation`, `sidebar-navigation`, `agent-gallery`

### Step 3: Generate Change ID

Create a verb-led change ID:
- For new screens: `add-{primary-capability}` (e.g., `add-task-creation`)
- For redesigns: `update-{primary-capability}` (e.g., `update-sidebar-layout`)
- If `$ARGUMENTS` includes a change name, use it

### Step 4: Generate Proposal

Create `openspec/changes/{change-id}/proposal.md`:

```markdown
## Why
[Describe the design intent — what problem does this UI solve?
Infer from the frame names, content, and component patterns.]

## What Changes
- [List each capability being added/modified]
- [Note the number of screens/states involved]
- [Highlight any reusable components introduced]

## Impact
- Affected specs: [list capabilities]
- Affected code: [infer file paths from component patterns]
  - Pages: `app/{route}/page.tsx`
  - Components: `components/{feature}/`
  - Layouts: `app/{route}/layout.tsx`
```

### Step 5: Generate Spec Deltas

For each capability, create `openspec/changes/{change-id}/specs/{capability}/spec.md`:

**Requirement generation rules:**

1. **Layout requirements**: For each major section in the frame
   ```markdown
   ### Requirement: Page Layout
   The page SHALL display a [layout description] with [sections].
   
   #### Scenario: Default layout
   - **WHEN** the user navigates to the page
   - **THEN** the page displays [sidebar/header/content] in [arrangement]
   - **AND** the sidebar width is [N]px
   ```

2. **Component requirements**: For each interactive component
   ```markdown
   ### Requirement: Search Input
   The page SHALL provide a search input in the [location].
   
   #### Scenario: Search placeholder
   - **WHEN** the search input is empty
   - **THEN** it displays placeholder text "[text from .pen]"
   ```

3. **State requirements**: When multiple frames show the same page in different states
   ```markdown
   ### Requirement: Dropdown Menu
   The [trigger] SHALL open a dropdown menu when clicked.
   
   #### Scenario: Menu opens
   - **WHEN** the user clicks the [trigger text]
   - **THEN** a dropdown menu appears with options: [list items from .pen]
   
   #### Scenario: Menu closes
   - **WHEN** the user clicks outside the menu
   - **THEN** the dropdown menu closes
   ```

4. **Navigation requirements**: For nav items, links, buttons that imply routing
   ```markdown
   ### Requirement: Sidebar Navigation
   The sidebar SHALL display navigation items: [list from .pen].
   
   #### Scenario: Navigate to section
   - **WHEN** the user clicks "[nav item text]"
   - **THEN** the application navigates to the [section] page
   - **AND** the clicked item is visually highlighted as active
   ```

5. **Visual requirements**: For styling that's critical to the design
   ```markdown
   ### Requirement: Dark Theme Styling
   The page SHALL use a dark theme with design tokens: [list key tokens].
   
   #### Scenario: Color consistency
   - **WHEN** the page renders
   - **THEN** backgrounds use the defined token colors
   - **AND** text uses the defined text color tokens
   ```

### Step 6: Generate Tasks

Create `openspec/changes/{change-id}/tasks.md`:

Map capabilities to implementation tasks:

```markdown
## 1. Setup
- [ ] 1.1 Create page route at `app/{route}/page.tsx`
- [ ] 1.2 Create layout at `app/{route}/layout.tsx` (if needed)

## 2. Components
- [ ] 2.1 Create `components/{feature}/{component}.tsx`
- [ ] 2.2 Create `components/{feature}/{component}.tsx`

## 3. Shared Components (if reusable components identified)
- [ ] 3.1 Create/update `components/shared/{component}.tsx`

## 4. Styling
- [ ] 4.1 Add design tokens to theme configuration
- [ ] 4.2 Verify dark theme consistency

## 5. Integration
- [ ] 5.1 Add route to navigation
- [ ] 5.2 Connect to data sources / API
- [ ] 5.3 Add loading/error states
```

### Step 7: Generate Design.md (if complex)

Create `openspec/changes/{change-id}/design.md` if:
- Multiple capabilities are involved
- Reusable components need shared architecture decisions
- State management patterns are non-obvious

### Step 8: Report

Print summary:
- Change ID and path
- Number of capabilities and requirements generated
- List of tasks
- Remind: "Review the proposal, then run `/studio-design:openspec-to-code {change-id}` to implement"

## Quality Checklist

- [ ] Every requirement has at least one `#### Scenario:` with `WHEN`/`THEN`
- [ ] Requirements use `SHALL`/`MUST` language
- [ ] Change ID is verb-led kebab-case
- [ ] Tasks are ordered logically (setup → components → integration)
- [ ] proposal.md has Why/What/Impact sections
- [ ] Frame states are captured as scenarios (not separate requirements)
- [ ] Reusable components are identified and factored out

## Does NOT

- Generate code — that's `openspec-to-code`
- Modify existing specs — only creates new change proposals
- Require OpenSpec CLI — generates files directly
- Handle backend/API design — focuses on UI requirements only
