# Pencil (.pen) Format Specification

## Overview

Pencil is a lightweight UI prototyping format stored as JSON. A `.pen` file describes UI screens (frames), their components, layout rules, and design tokens.

## Top-Level Structure

```json
{
  "version": "2.10",
  "children": [ /* array of Frame nodes — each is a screen/page */ ],
  "variables": { /* design tokens (colors, etc.) */ }
}
```

## Node Types

### 1. `frame` — Container / Screen

The primary layout container. Top-level frames represent screens/pages.

```json
{
  "type": "frame",
  "id": "unique-id",
  "name": "Screen Name",
  "x": 0, "y": 0,
  "width": 1440,
  "height": 900,
  "fill": "#09090B",
  "stroke": "#27272A",
  "strokeWidth": 1,
  "cornerRadius": 8,
  "opacity": 1.0,
  "layout": "vertical",
  "gap": 8,
  "padding": [16, 16, 16, 16],
  "alignItems": "center",
  "justifyContent": "start",
  "children": [],
  "reusable": true,
  "visible": true
}
```

**Sizing values for width/height:**
- Number → fixed pixels
- `"fill_container"` → flex: 1 (stretch to fill parent)
- `"fit_content"` → auto-size to children

### 2. `text` — Text Element

```json
{
  "type": "text",
  "id": "unique-id",
  "content": "Display text here",
  "fontFamily": "Inter",
  "fontSize": 14,
  "fontWeight": 400,
  "lineHeight": 1.5,
  "letterSpacing": 0,
  "fill": "$text-primary",
  "textAlign": "left",
  "width": "fit_content",
  "height": "fit_content"
}
```

### 3. `icon_font` — Icon Element

```json
{
  "type": "icon_font",
  "id": "unique-id",
  "iconFontName": "panel-left",
  "iconFontFamily": "lucide",
  "width": 18,
  "height": 18,
  "fill": "$text-secondary"
}
```

### 4. `ellipse` — Circle / Oval

```json
{
  "type": "ellipse",
  "id": "unique-id",
  "width": 12,
  "height": 12,
  "fill": "#FF5F57"
}
```

### 5. `ref` — Component Reference

```json
{
  "type": "ref",
  "id": "unique-id",
  "ref": "cwxcX",
  "x": 0, "y": 0,
  "descendants": {
    "child-id-1": { "content": "Override text" },
    "child-id-2": { "fill": "#FF0000", "visible": false }
  }
}
```

## Variables (Design Tokens)

```json
{
  "variables": {
    "$token-name": { "type": "color", "value": "#hex-value" }
  }
}
```

**Standard dark theme tokens:**

| Token | Value | Usage |
|-------|-------|-------|
| `$bg` | `#09090B` | Main background |
| `$bg-sidebar` | `#0C0C0E` | Sidebar background |
| `$bg-card` | `#111113` | Card background |
| `$bg-input` | `#1C1C22` | Input field background |
| `$bg-muted` | `#1A1A1F` | Muted/hover background |
| `$text-primary` | `#FAFAFA` | Primary text |
| `$text-secondary` | `#A1A1AA` | Secondary text |
| `$text-muted` | `#71717A` | Muted/placeholder text |
| `$accent` | `#3B82F6` | Accent/primary action |
| `$border` | `#27272A` | Default border |
| `$destructive` | `#EF4444` | Error/destructive |

## Layout System

When a frame has `layout: "vertical"` or `"horizontal"`:
- Children flow in the specified direction
- `gap` controls spacing between children
- `padding` controls internal padding
- `alignItems` controls cross-axis alignment
- Children with `"fill_container"` sizing stretch to fill

When no `layout` property: children use `x`, `y` for absolute positioning.

## Reusable Components

1. Define: set `"reusable": true` on a frame
2. Reference: use `"type": "ref"` pointing to the component's `id`
3. Override: use `descendants` map to change nested properties

## ID Generation

Use 5-character alphanumeric IDs (e.g., `aEZUg`, `tFU4O`). Generate randomly.

## Best Practices

1. Always use `$variable` references for colors instead of hardcoded hex
2. Prefer auto layout (`layout` + `gap`) over absolute positioning
3. Name top-level frames descriptively: "1. New Task (Empty State)"
4. Standard desktop: 1440×900, mobile: 390×844
5. Use Lucide icon names from the `lucide` font family
