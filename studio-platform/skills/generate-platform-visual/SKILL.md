---
name: generate-platform-visual
description: Generate a .pen visualization file for the industry AI model platform — a 4-frame design containing dashboard overview, agent roster, knowledge network, and application scenarios. Creates a visual presentation artifact by cloning a reference template or building from scratch.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
user-invocable: true
---

### Overview
The .pen visualization file is a JSON-based design document used for platform presentations. It contains 4 frames that visually represent the platform's capabilities. This is Step 5 of the platform documentation pipeline.

### .pen File Format
The .pen format is a JSON structure with:
```json
{
  "version": "2.10",
  "children": [
    { "type": "frame", "children": [...] },  // Frame 0: Dashboard
    { "type": "frame", "children": [...] },  // Frame 1: Agents
    { "type": "frame", "children": [...] },  // Frame 2: Knowledge Network
    { "type": "frame", "children": [...] }   // Frame 3: Application Scenarios
  ]
}
```

Each frame contains nested text nodes with properties:
- `id`: unique identifier
- `type`: "frame" or "text"
- `content`: text content (the part we generate)
- `x`, `y`, `width`, `height`: position and size
- `fontSize`, `fontWeight`: typography
- `fill`: background color
- Visual properties are preserved from reference; only `content` is replaced.

### Inputs Required
1. **All generated docs**: brainmap-index.md, agent-mapping, tech designs, project plan
2. **Reference .pen file** (optional): a .pen file from a similar project to use as layout template
3. **Platform configuration**: platform name, industry, key statistics

### 4 Frame Structure

#### Frame 0: 全景驾驶舱 (Dashboard)
- Header: platform name + tagline
- KPI row: total agents, plugins, skills, data assets, knowledge docs
- Body: 4 capability quadrants (service domains)
- Footer: technology stack summary

#### Frame 1: 角色智能体 (Agent Roster)  
- Header: "{N}个专业智能体"
- Body: module cards, each listing agents with numbers and names
- Organized by service domain (e.g., 保育健康域, 教育发展域, etc.)
- Statistics: agent count per domain, total skill count

#### Frame 2: 知识网络 (Knowledge Network)
- Header: "知识网络"
- Body: knowledge base categories with document counts
- Sub-graphs listing with entity/relation counts
- Data asset summary (policies, standards, assessment tools, etc.)

#### Frame 3: 数智场景 (Application Scenarios)
- Header: "数智场景应用"  
- Body: scenario cards organized by service endpoint (G/B/C)
- Each scenario: name, description, participating agents

### Workflow

#### Approach A: Clone from Reference (preferred when reference exists)
1. Read reference .pen file (e.g., from a previous industry project)
2. Parse JSON structure, identify all text nodes
3. Build node-ID → content mapping
4. Generate new content for each node based on current platform's data
5. Replace content in the cloned structure
6. Write output .pen file

For this approach, generate a Python script that:
- Deep-clones the reference JSON
- Walks all nodes recursively
- Replaces text content based on a mapping dictionary
- Validates output JSON

#### Approach B: Build from Scratch
1. Define frame dimensions and layout
2. Create text nodes with positioning based on content volume
3. Style with appropriate colors and typography
4. Write output .pen file

### Output Location
`{output_dir}/{platform_name}.pen`

### Quality Checks
1. Valid JSON (parseable without errors)
2. All 4 frames present
3. No residual text from reference template (search for industry-specific terms from reference)
4. Statistics in frames match brainmap-index.md totals
5. All agents referenced in Frame 1 exist in brainmap
6. File size reasonable (200KB-500KB typical)

### Does NOT
- Create the layout design from scratch (uses reference template)
- Generate interactive presentations (static design file only)
- Export to other visual formats (PDF, PNG, etc.)
