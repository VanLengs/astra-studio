#!/usr/bin/env python3
"""Validate all skills within a plugin directory.

Usage:
    python validate_skills.py <plugin-dir>

Checks per skill:
    - SKILL.md exists
    - YAML frontmatter is valid
    - Required frontmatter fields: name, description
    - name matches directory name
    - description is under 1024 chars
    - Warns on unknown frontmatter keys
    - Warns if SKILL.md exceeds 500 lines
    - Referenced scripts/ files exist
    - Referenced references/ files exist
"""

import json
import re
import sys
from pathlib import Path


KNOWN_FRONTMATTER_KEYS = {
    "name",
    "description",
    "allowed-tools",
    "user-invocable",
    "disabled",
    "trigger",
    "model",
}


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from SKILL.md. Returns (metadata, body)."""
    if not text.startswith("---"):
        return {}, text

    end = text.find("---", 3)
    if end == -1:
        return {}, text

    frontmatter_text = text[3:end].strip()
    body = text[end + 3 :].strip()

    # Simple YAML parser for flat key-value pairs
    metadata = {}
    for line in frontmatter_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r"^([a-zA-Z_-]+)\s*:\s*(.+)$", line)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            # Remove quotes
            if (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")
            ):
                value = value[1:-1]
            # Parse booleans
            if value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            metadata[key] = value

    return metadata, body


def validate_skill(skill_dir: Path) -> dict:
    """Validate a single skill directory. Returns {name, passed, failed, warnings}."""
    results = {
        "name": skill_dir.name,
        "passed": [],
        "failed": [],
        "warnings": [],
    }

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        results["failed"].append("SKILL.md not found")
        return results
    results["passed"].append("SKILL.md exists")

    text = skill_md.read_text()
    lines = text.splitlines()

    # Line count check
    if len(lines) > 500:
        results["warnings"].append(f"SKILL.md is {len(lines)} lines (recommend < 500)")
    else:
        results["passed"].append(f"SKILL.md is {len(lines)} lines (< 500)")

    # Parse frontmatter
    metadata, body = parse_frontmatter(text)
    if not metadata:
        results["failed"].append("No valid YAML frontmatter found")
        return results
    results["passed"].append("YAML frontmatter is valid")

    # Required fields
    name = metadata.get("name", "")
    if name:
        results["passed"].append(f"'name' field present: {name}")
    else:
        results["failed"].append("'name' field missing in frontmatter")

    description = metadata.get("description", "")
    if description:
        if len(str(description)) <= 1024:
            results["passed"].append("'description' present and under 1024 chars")
        else:
            results["failed"].append(
                f"'description' is {len(str(description))} chars (max 1024)"
            )
    else:
        results["failed"].append("'description' field missing in frontmatter")

    # Name matches directory
    if name and name == skill_dir.name:
        results["passed"].append(f"Skill name matches directory name '{skill_dir.name}'")
    elif name:
        results["warnings"].append(
            f"Skill name '{name}' does not match directory name '{skill_dir.name}'"
        )

    # Unknown frontmatter keys
    unknown_keys = set(metadata.keys()) - KNOWN_FRONTMATTER_KEYS
    if unknown_keys:
        results["warnings"].append(f"Unknown frontmatter keys: {', '.join(sorted(unknown_keys))}")

    # Check referenced scripts
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.is_dir():
        for script in scripts_dir.iterdir():
            if script.is_file():
                results["passed"].append(f"Script exists: scripts/{script.name}")

    # Check for script references in body that don't exist (skip runtime variable paths)
    for match in re.finditer(r"scripts/([a-zA-Z0-9_.-]+\.py)", body):
        ref = match.group(1)
        start = max(0, match.start() - 50)
        context = body[start:match.start()]
        if "${CLAUDE_SKILL_DIR}" in context:
            continue
        script_path = skill_dir / "scripts" / ref
        if not script_path.exists():
            results["failed"].append(f"Referenced script 'scripts/{ref}' not found")

    # Check referenced files in references/
    refs_dir = skill_dir / "references"
    if refs_dir.is_dir():
        for ref_file in refs_dir.iterdir():
            if ref_file.is_file():
                results["passed"].append(f"Reference exists: references/{ref_file.name}")

    # Check references/ mentions that are local (not ${CLAUDE_SKILL_DIR} paths)
    for match in re.finditer(r"references/([a-zA-Z0-9_.-]+\.md)", body):
        ref = match.group(1)
        # Skip references using runtime variables (e.g., ${CLAUDE_SKILL_DIR}/../../references/)
        start = max(0, match.start() - 50)
        context = body[start:match.start()]
        if "${CLAUDE_SKILL_DIR}" in context:
            continue
        ref_path = skill_dir / "references" / ref
        if not ref_path.exists():
            results["failed"].append(f"Referenced file 'references/{ref}' not found")

    return results


def validate_skills(plugin_dir: str) -> list[dict]:
    """Validate all skills in a plugin directory."""
    root = Path(plugin_dir).resolve()

    # Find skills directory
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return [{"name": "(none)", "failed": ["No skills/ directory found"], "passed": [], "warnings": []}]

    results = []
    for skill_dir in sorted(skills_dir.iterdir()):
        if skill_dir.is_dir() and not skill_dir.name.startswith("."):
            results.append(validate_skill(skill_dir))

    if not results:
        return [{"name": "(none)", "failed": ["No skill directories found in skills/"], "passed": [], "warnings": []}]

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_skills.py <plugin-dir>", file=sys.stderr)
        sys.exit(1)

    plugin_dir = sys.argv[1]
    if not Path(plugin_dir).is_dir():
        print(f"Error: '{plugin_dir}' is not a directory", file=sys.stderr)
        sys.exit(1)

    results = validate_skills(plugin_dir)
    print(json.dumps(results, indent=2))

    has_failures = any(r["failed"] for r in results)
    if has_failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
