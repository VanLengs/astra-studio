#!/usr/bin/env python3
"""Generate a combined validation report from individual check results.

Usage:
    python generate_report.py <plugin-dir>

Runs all validators and produces a formatted summary report.
"""

import json
import subprocess
import sys
from pathlib import Path


def run_validator(script: str, plugin_dir: str) -> dict:
    """Run a validator script and capture its JSON output."""
    script_path = Path(__file__).parent / script
    try:
        result = subprocess.run(
            [sys.executable, str(script_path), plugin_dir],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return json.loads(result.stdout) if result.stdout.strip() else {}
    except (json.JSONDecodeError, subprocess.TimeoutExpired, FileNotFoundError) as e:
        return {"error": str(e)}


def format_report(plugin_name: str, structure: dict, skills: list, deps: dict) -> str:
    """Format the validation results into a readable report."""
    lines = []
    lines.append(f"Plugin Validation: {plugin_name}")
    lines.append("=" * (len(lines[0]) + 2))
    lines.append("")

    # Structure summary
    s_pass = len(structure.get("passed", []))
    s_fail = len(structure.get("failed", []))
    s_warn = len(structure.get("warnings", []))
    s_total = s_pass + s_fail
    s_icon = "FAIL" if s_fail else ("WARN" if s_warn else "PASS")
    lines.append(f"Structure:    {s_icon}  {s_pass}/{s_total} passed" + (f" ({s_warn} warnings)" if s_warn else ""))

    # Skills summary
    total_skill_pass = sum(len(s.get("passed", [])) for s in skills)
    total_skill_fail = sum(len(s.get("failed", [])) for s in skills)
    total_skill_warn = sum(len(s.get("warnings", [])) for s in skills)
    total_skill_checks = total_skill_pass + total_skill_fail
    sk_icon = "FAIL" if total_skill_fail else ("WARN" if total_skill_warn else "PASS")
    lines.append(
        f"Skills:       {sk_icon}  {total_skill_pass}/{total_skill_checks} passed"
        + (f" ({total_skill_warn} warnings)" if total_skill_warn else "")
    )

    # Dependencies summary
    d_pass = len(deps.get("passed", []))
    d_fail = len(deps.get("failed", []))
    d_warn = len(deps.get("warnings", []))
    d_total = d_pass + d_fail
    d_icon = "FAIL" if d_fail else ("WARN" if d_warn else "PASS")
    lines.append(f"Dependencies: {d_icon}  {d_pass}/{d_total} passed" + (f" ({d_warn} warnings)" if d_warn else ""))

    lines.append("")

    # Failures
    all_failures = []
    for item in structure.get("failed", []):
        all_failures.append(f"  [structure] {item}")
    for skill in skills:
        for item in skill.get("failed", []):
            all_failures.append(f"  [skill:{skill.get('name', '?')}] {item}")
    for item in deps.get("failed", []):
        all_failures.append(f"  [dependency] {item}")

    if all_failures:
        lines.append("Errors:")
        lines.extend(all_failures)
        lines.append("")

    # Warnings
    all_warnings = []
    for item in structure.get("warnings", []):
        all_warnings.append(f"  [structure] {item}")
    for skill in skills:
        for item in skill.get("warnings", []):
            all_warnings.append(f"  [skill:{skill.get('name', '?')}] {item}")
    for item in deps.get("warnings", []):
        all_warnings.append(f"  [dependency] {item}")

    if all_warnings:
        lines.append("Warnings:")
        lines.extend(all_warnings)
        lines.append("")

    # Overall verdict
    has_failures = bool(all_failures)
    has_warnings = bool(all_warnings)
    if has_failures:
        verdict = "FAIL"
    elif has_warnings:
        verdict = "PASS (with warnings)"
    else:
        verdict = "PASS"
    lines.append(f"Overall: {verdict}")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_report.py <plugin-dir>", file=sys.stderr)
        sys.exit(1)

    plugin_dir = sys.argv[1]
    root = Path(plugin_dir).resolve()
    if not root.is_dir():
        print(f"Error: '{plugin_dir}' is not a directory", file=sys.stderr)
        sys.exit(1)

    plugin_name = root.name

    # Run validators
    structure = run_validator("validate_plugin.py", plugin_dir)
    skills_raw = run_validator("validate_skills.py", plugin_dir)
    deps = run_validator("check_dependencies.py", plugin_dir)

    # Skills returns a list
    skills = skills_raw if isinstance(skills_raw, list) else [skills_raw]

    # Generate report
    report = format_report(plugin_name, structure, skills, deps)
    print(report)

    # Output JSON for programmatic consumption
    json_result = {
        "plugin": plugin_name,
        "structure": structure,
        "skills": skills,
        "dependencies": deps,
        "verdict": "FAIL" if any([
            structure.get("failed"),
            any(s.get("failed") for s in skills),
            deps.get("failed"),
        ]) else "PASS",
    }
    json_path = root / ".validation-report.json"
    json_path.write_text(json.dumps(json_result, indent=2) + "\n")
    print(f"\nJSON report saved to: {json_path}")

    if json_result["verdict"] == "FAIL":
        sys.exit(1)


if __name__ == "__main__":
    main()
