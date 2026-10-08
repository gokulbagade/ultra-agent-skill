# 🧪 Agentic Workflow 06: Test-Driven Development (TDD)

> **Purpose:** Enforce ironclad Red-Green-Refactor discipline. No production code is written without a failing test first.

---

## 📋 Prerequisites
- A test framework installed and configured (`pytest`, `vitest`, `jest`, `cargo test`, etc.).
- Concrete behavioral requirement or acceptance criteria from `@planner`.
- Target function signatures or API contracts defined.

---

## 🧭 Workflow State Machine

```mermaid
graph TD
    A["Requirement / Spec"] --> B["1. RED: Write Failing Test"]
    B --> C["2. VERIFY RED: Run Test & Confirm Failure"]
    C --> D["3. GREEN: Write Minimal Implementation"]
    D --> E["4. VERIFY GREEN: Run Test & Confirm Pass"]
    E --> F["5. REFACTOR: Clean Code & Keep Green"]
    F --> G{"Next Requirement?"}
    G -->|"Yes"| B
    G -->|"No"| H["Full Suite Verification"]
```

---

## Step-by-Step Execution

### Step 1: Write Atomic Failing Test (RED)
- Write a single unit or integration test representing one atomic requirement.
- Test against real code where possible (avoid artificial mocks unless testing external I/O or network calls).
- Name the test clearly following the `test_[scenario]_[expected_outcome]` convention.

### Step 2: Verify RED State
- Run the test suite:
  ```bash
  pytest tests/test_feature.py
  # or
  npm test
  ```
- **Inspect failure message:** Confirm the test fails for the *expected reason* (e.g. missing function or incorrect return value), not because of syntax or import errors.

### Step 3: Implement Minimal Solution (GREEN)
- Apply the **Ponytail Principle**: Write the simplest code that allows the test to pass.
- Do not add unrequested helper methods, speculative abstractions, or future-proofing logic.

### Step 4: Verify GREEN State
- Re-run the test command.
- Confirm that the new test passes and all pre-existing tests remain green (0 failures).

### Step 5: Refactor
- Remove duplication.
- Improve naming and readability.
- Re-run tests after refactoring to ensure no regressions were introduced.

---

## ⚖️ The Iron Rules of TDD
1. Production code written before tests must be deleted.
2. "I will write tests after" is strictly prohibited. Tests written after implementation pass immediately and prove nothing about the test's validity.

---

## 🔗 Related Workflows
- **Prerequisite:** [Workflow 12: Implementation Planning & Checklists](12-implementation-planning-and-checklists.md)
- **Subagent Execution:** [Workflow 02: Subagent-Driven Development](02-subagent-driven-development.md)
- **Bug Remediation:** [Workflow 05: Systematic Root Cause Debugging](05-systematic-root-cause-debugging.md)
- **Gate Enforcement:** [Workflow 10: Gate-Function Verification](10-gate-function-verification.md)
