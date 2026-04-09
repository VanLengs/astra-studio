---
description: Run the full design-to-code pipeline — screenshot → Pencil prototype → OpenSpec proposal → working code
argument-hint: [screenshot path or .pen path]
---

Run the complete design-to-code pipeline for `$ARGUMENTS`.

This command chains three skills in sequence, with a human review checkpoint between each stage:

## Pipeline

1. **Screenshot → Pencil** (`screenshot-to-pencil`)
   - Analyze the UI screenshot and generate a `.pen` prototype file
   - ⏸️ Pause for review — user confirms the .pen output before proceeding

2. **Pencil → OpenSpec** (`pencil-to-openspec`)
   - Parse the .pen file and generate an OpenSpec change proposal
   - ⏸️ Pause for review — user confirms the proposal before proceeding

3. **OpenSpec → Code** (`openspec-to-code`)
   - Implement the approved proposal as React/Next.js code

## Usage

- Full pipeline from screenshot: `/studio-design:design path/to/screenshot.png`
- Start from existing .pen: `/studio-design:design path/to/prototype.pen`
- Start from existing OpenSpec change: `/studio-design:design openspec-change-id`

The pipeline auto-detects the input type and starts from the appropriate stage.

Use skills: "screenshot-to-pencil", "pencil-to-openspec", "openspec-to-code" in sequence.
