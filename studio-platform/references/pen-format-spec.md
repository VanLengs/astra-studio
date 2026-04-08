# .pen File Format Specification

This reference documents the .pen visualization file format used for platform presentation designs.

## Format Overview

The .pen format is a JSON-based design file used for creating visual presentation boards. Each file contains frames (pages/canvases) with nested visual elements.

## JSON Structure

```json
{
  "version": "2.10",
  "type": "design",
  "children": [
    {
      "type": "frame",
      "id": "frame-0",
      "name": "Frame Name",
      "x": 0,
      "y": 0,
      "width": 1920,
      "height": 1080,
      "children": [
        {
          "type": "text",
          "id": "text-001",
          "content": "Display text content",
          "x": 100,
          "y": 50,
          "width": 400,
          "height": 60,
          "fontSize": 24,
          "fontWeight": "bold",
          "fill": "#1a1a2e",
          "color": "#ffffff"
        }
      ]
    }
  ]
}
```

## Node Types

### Frame
Top-level container (equivalent to a slide/canvas):
- `type`: "frame"
- `id`: unique identifier
- `name`: frame label
- `x`, `y`: position
- `width`, `height`: canvas dimensions (typically 1920×1080 or larger)
- `children`: nested elements

### Text
Text content node:
- `type`: "text"
- `id`: unique identifier (used for content replacement)
- `content`: the actual text to display
- `x`, `y`: position within parent
- `width`, `height`: bounding box
- `fontSize`: text size in points
- `fontWeight`: "normal", "bold", "600", etc.
- `fill`: background color (hex)
- `color`: text color (hex)

### Group
Container for grouping elements:
- `type`: "group"
- `id`: unique identifier
- `children`: nested elements
- Groups preserve relative positioning

## Standard 4-Frame Layout

Platform documentation uses a standardized 4-frame layout:

### Frame 0: 全景驾驶舱 (Dashboard)
**Purpose**: High-level platform overview with KPI metrics

**Layout structure**:
```
┌────────────────────────────────────────────┐
│  Header: Platform name + tagline           │
├────────────────────────────────────────────┤
│  KPI Row: [Agents] [Plugins] [Skills] [Data] │
├──────────────────┬─────────────────────────┤
│  Domain 1        │  Domain 2              │
│  capabilities    │  capabilities          │
├──────────────────┼─────────────────────────┤
│  Domain 3        │  Domain 4              │
│  capabilities    │  capabilities          │
├────────────────────────────────────────────┤
│  Footer: Tech stack / data assets summary  │
└────────────────────────────────────────────┘
```

### Frame 1: 角色智能体 (Agent Roster)
**Purpose**: Showcase all AI agents organized by module/domain

**Layout structure**:
```
┌────────────────────────────────────────────┐
│  Header: "{N}个专业智能体"                   │
├────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ Domain 1 │ │ Domain 2 │ │ Domain 3 │  │
│  │ Module A │ │ Module C │ │ Module E │  │
│  │ agents...│ │ agents...│ │ agents...│  │
│  │ Module B │ │ Module D │ │ Module F │  │
│  │ agents...│ │ agents...│ │ agents...│  │
│  └──────────┘ └──────────┘ └──────────┘  │
├────────────────────────────────────────────┤
│  Footer: Total stats                       │
└────────────────────────────────────────────┘
```

### Frame 2: 知识网络 (Knowledge Network)
**Purpose**: Display the knowledge infrastructure

**Layout structure**:
```
┌────────────────────────────────────────────┐
│  Header: "知识网络"                         │
├────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────────────────┐   │
│  │ Sub-graph│  │ Knowledge base       │   │
│  │ overview │  │ categories & counts  │   │
│  └──────────┘  └──────────────────────┘   │
│  ┌──────────────────────────────────────┐ │
│  │ Entity types / relations summary     │ │
│  └──────────────────────────────────────┘ │
├────────────────────────────────────────────┤
│  Footer: Total triples / docs / chunks     │
└────────────────────────────────────────────┘
```

### Frame 3: 数智场景 (Application Scenarios)
**Purpose**: Show concrete application scenarios by endpoint

**Layout structure**:
```
┌────────────────────────────────────────────┐
│  Header: "数智场景应用"                      │
├──────────┬──────────┬──────────┬──────────┤
│  G端     │  B端     │  C端     │  产业端   │
│  Gov     │  Biz     │  Consumer│  Industry │
│  场景1   │  场景1   │  场景1   │  场景1    │
│  场景2   │  场景2   │  场景2   │  场景2    │
│  场景3   │  场景3   │  场景3   │  场景3    │
│  ...     │  ...     │  ...     │  ...      │
└──────────┴──────────┴──────────┴──────────┘
```

## Content Replacement Strategy

When cloning from a reference .pen file:

1. **Parse** the reference JSON
2. **Walk** all nodes recursively
3. **Identify** text nodes (type === "text")
4. **Map** each node's content to new content based on:
   - Position in frame (header, KPI, body, footer)
   - Node ID pattern
   - Content pattern matching
5. **Replace** content while preserving all visual properties
6. **Validate** no residual text from the reference industry remains

### Python Script Pattern

```python
import json, copy

def deep_replace(node, content_map):
    """Recursively replace text content in .pen nodes."""
    if isinstance(node, dict):
        if node.get('type') == 'text' and 'content' in node:
            node_id = node.get('id', '')
            if node_id in content_map:
                node['content'] = content_map[node_id]
        if 'children' in node:
            for child in node['children']:
                deep_replace(child, content_map)
    elif isinstance(node, list):
        for item in node:
            deep_replace(item, content_map)

# Load reference
with open('reference.pen', 'r') as f:
    data = json.load(f)

# Deep clone
new_data = copy.deepcopy(data)

# Build content map from platform data
content_map = build_content_map(platform_data)

# Replace
deep_replace(new_data, content_map)

# Write output
with open('output.pen', 'w') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)
```

## Validation Checklist

- [ ] Valid JSON (no parse errors)
- [ ] Correct frame count (4)
- [ ] All text nodes have content
- [ ] No empty content strings
- [ ] No residual reference industry terms
- [ ] Statistics match brainmap totals
- [ ] File size in expected range (200KB-500KB)
