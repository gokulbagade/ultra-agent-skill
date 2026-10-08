#!/usr/bin/env python3
"""
plan_validator.py — Implementation Plan Schema & Structure Validator
Validates implementation plans against §11 standards:
- Requires sections: Goal, Architecture, Tech Stack, Affected Files, Checklist.
- Validates checkbox syntax (- [ ] or - [x]).
- Warns if task count > 20 (requires sub-plan decomposition).
- Checks whether referenced files exist in repository.
- Outputs structured JSON or formatted terminal summary.
"""

import sys
import re
import json
import argparse
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


REQUIRED_SECTIONS = [
    ("Goal", re.compile(r"^#+\s*(?:Goal|Technical Objective|Objective)", re.MULTILINE | re.IGNORECASE)),
    ("Architecture", re.compile(r"^#+\s*(?:Architecture|Design|System Architecture)", re.MULTILINE | re.IGNORECASE)),
    ("Tech Stack", re.compile(r"^#+\s*(?:Tech Stack|Technology Stack|Stack)", re.MULTILINE | re.IGNORECASE)),
    ("Affected Files", re.compile(r"^#+\s*(?:Affected Files|Target Files|Files Modified)", re.MULTILINE | re.IGNORECASE)),
    ("Master Checklist", re.compile(r"^#+\s*(?:Master Checklist|Tasks|Checklist|Implementation Steps)", re.MULTILINE | re.IGNORECASE)),
]


def validate_plan(plan_path: Path, workspace_root: Path = None) -> dict:
    if not plan_path.exists():
        return {
            "valid": False,
            "errors": [f"Plan file not found: {plan_path}"],
            "warnings": [],
            "stats": {},
        }

    try:
        content = plan_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return {
            "valid": False,
            "errors": [f"Failed to read plan file: {e}"],
            "warnings": [],
            "stats": {},
        }

    errors = []
    warnings = []

    # 1. Section Presence Validation
    for section_name, pattern in REQUIRED_SECTIONS:
        if not pattern.search(content):
            errors.append(f"Missing required section: '{section_name}'")

    # 2. Checkbox Syntax & Count Validation
    checklist_pattern = re.compile(r"^\s*-\s*\[([ xX])\]\s+(.*)$", re.MULTILINE)
    matches = checklist_pattern.findall(content)

    total_tasks = len(matches)
    completed_tasks = sum(1 for m in matches if m[0] in ("x", "X"))
    pending_tasks = total_tasks - completed_tasks

    if total_tasks == 0:
        errors.append("No checklist items found. Plans must include atomic task checklists with '- [ ]'.")
    elif pending_tasks > 20:
        warnings.append(
            f"Plan contains {pending_tasks} pending tasks (>20 limit). Decompose into sub-plans for better agent context retention."
        )

    # 3. File Verification Check
    # Look for files listed under Affected Files section or backtick paths
    file_references = re.findall(r"`([^`]+\.[a-zA-Z0-9_-]+)`", content)
    missing_files = []
    if workspace_root and workspace_root.exists():
        for ref in file_references:
            # Skip wildcards, URLs, generic packages, or obvious non-files
            if any(ref.startswith(p) for p in ("http", "git", "/", "\\")) or "*" in ref or " " in ref:
                continue
            cand_path = workspace_root / ref
            # If path doesn't exist and not annotated as (New) or (Create)
            if not cand_path.exists():
                # Check if marked as new in the text
                if not re.search(rf"`{re.escape(ref)}`\s*(?:\((?:new|create|to be created)\)|-\s*new)", content, re.IGNORECASE):
                    missing_files.append(ref)

    if missing_files:
        warnings.append(f"Referenced files not found on disk (mark as '(new)' if to be created): {', '.join(missing_files[:5])}")

    is_valid = len(errors) == 0

    return {
        "valid": is_valid,
        "plan_file": str(plan_path),
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "completion_percentage": round((completed_tasks / total_tasks * 100), 1) if total_tasks else 0,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Validate implementation plan against §11 specification schema.")
    parser.add_argument("plan_file", help="Path to markdown implementation plan")
    parser.add_argument("--workspace", default=".", help="Root directory of workspace to verify file paths")
    parser.add_argument("--json", action="store_true", help="Output machine-parseable JSON")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")

    args = parser.parse_args()
    plan_path = Path(args.plan_file)
    workspace = Path(args.workspace)

    result = validate_plan(plan_path, workspace)

    if args.strict and result["warnings"]:
        result["valid"] = False
        result["errors"].extend(result["warnings"])

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"📋 Implementation Plan Validation: {plan_path.name}")
        stats = result.get("stats", {})
        if stats:
            print(f"  • Tasks: {stats.get('completed_tasks')}/{stats.get('total_tasks')} complete ({stats.get('completion_percentage')}%)")

        if result["valid"]:
            print("✅ Plan adheres to §11 schema.")
        else:
            print("❌ Plan validation failed:")
            for err in result["errors"]:
                print(f"   • ERROR: {err}")

        for warn in result["warnings"]:
            print(f"   ⚠️ WARNING: {warn}")

    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
