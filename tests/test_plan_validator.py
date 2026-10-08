#!/usr/bin/env python3
"""
Unit tests for plan_validator.py
"""

import sys
import unittest
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from plan_validator import validate_plan


class TestPlanValidator(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.dir_path = Path(self.test_dir.name)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_valid_plan_passes_schema(self):
        plan_file = self.dir_path / "valid_plan.md"
        plan_file.write_text("""# 📋 Feature Implementation Plan

## Goal
Implement a resilient webhook dispatch pipeline.

## Architecture & Strategy
Use Event router with retry queues.

## Tech Stack
FastAPI, Redis, Pydantic.

## Affected Files
- `app/webhook.py` (new)
- `tests/test_webhook.py` (new)

## Master Checklist
### Phase 1: Setup
- [ ] Step 1: Write failing test (RED)
- [x] Step 2: Implement minimal code (GREEN)
- [ ] Step 3: Run gate verification
""", encoding="utf-8")

        result = validate_plan(plan_file, self.dir_path)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)
        self.assertEqual(result["stats"]["total_tasks"], 3)
        self.assertEqual(result["stats"]["completed_tasks"], 1)

    def test_missing_sections_flags_errors(self):
        plan_file = self.dir_path / "incomplete_plan.md"
        plan_file.write_text("""# Incomplete Plan
Just some notes without proper sections.
- [ ] Task 1
""", encoding="utf-8")

        result = validate_plan(plan_file, self.dir_path)
        self.assertFalse(result["valid"])
        self.assertTrue(any("Missing required section" in err for err in result["errors"]))

    def test_task_count_over_20_triggers_warning(self):
        tasks = "\n".join(f"- [ ] Atomic task {i}" for i in range(25))
        plan_file = self.dir_path / "large_plan.md"
        plan_file.write_text(f"""# 📋 Large Plan
## Goal
Large migration initiative.
## Architecture
Modular microservices.
## Tech Stack
Node.js, PostgreSQL.
## Affected Files
- `index.ts`
## Master Checklist
{tasks}
""", encoding="utf-8")

        result = validate_plan(plan_file, self.dir_path)
        self.assertTrue(any(">20 limit" in w for w in result["warnings"]))


if __name__ == "__main__":
    unittest.main()
