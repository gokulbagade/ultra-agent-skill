# ⚡ Ultra Skill v4.0 — Universal AI Agent Architecture & Rules

> **Master Directive:** Read and follow [skills/ultra-skill/SKILL.md](file:///d:/Agent%20SKILLS/ultra-skill/skills/ultra-skill/SKILL.md) for every task. Execute via the deterministic 6-phase Agentic State Machine.

---

## 🧭 The 6-Phase Agentic State Machine

1. **State 0: Intake & Intent Routing:** Classify request domain, bind active subagent roles, and map applicable reference manuals.
2. **State 1: Reconnaissance & Fact-Gathering:** Audit code, dependencies, and interfaces before authoring any diff. Formulate Design Read (Frontend) or Trace Log (ADK).
3. **State 2: Mandatory Plan & Interactive Checklist (Iron Law):** Whenever ANY new plan or task starts, you MUST author a structured Implementation Plan, validate schema via `python scripts/plan_validator.py`, and generate an interactive markdown checklist (`- [ ]`) before writing code. Track progress in real-time.
4. **State 3: Subagent Execution:** Apply Ponytail Ladder (shortest working diff), Red-Green-Refactor TDD discipline, and file partition ownership for parallel dispatches.
5. **State 4: Autonomous Review & Correction:** Run CodeRabbit security scan, classify issues (Critical → Info), audit contrast via `python scripts/contrast_checker.py`, run slop detector (`python scripts/detect_ai_slop.py`), and recover via Workflow 13 if errors occur.
6. **State 5: Gate-Function Verification:** Execute fresh terminal verification commands via `python scripts/verify_evidence.py --json --save .verification/receipt.json`. Exit code `0` and zero failures required before claiming completion.

---

## 📋 The Iron Law of Planning & Checklists

```
NO CODE CHANGES OR FILE CREATION WITHOUT AN IMPLEMENTATION PLAN AND CHECKLIST FIRST
```

Whenever a new task or plan begins:
1. **Author the Implementation Plan:** Outline the goal, architecture, tech stack, affected file paths, and interfaces.
2. **Validate Plan Schema:** Run `python scripts/plan_validator.py <plan.md>` to verify compliance and task count ($\le 20$).
3. **Generate the Interactive Checklist:** Every milestone and atomic task MUST use checkable markdown checkboxes (`- [ ]`).
4. **Live Progress Tracking:** As each step passes verification, update the checkbox to `- [x]`.
5. **Never Check Ahead:** Only check items off AFTER receiving fresh terminal execution proof.

---

## 👥 Subagent Roles & Personas

When executing specialized tasks, assume or dispatch these dedicated subagent roles:
- **`@planner`** ([agents/planner.md](file:///d:/Agent%20SKILLS/ultra-skill/agents/planner.md)): Zero-context implementation plans, spec synthesis, risk matrix, and progress checklists.
- **`@architect`** ([agents/architect.md](file:///d:/Agent%20SKILLS/ultra-skill/agents/architect.md)): Google ADK 2.0 graphs, dynamic nodes, state channels, resilience, and circuit breakers.
- **`@visualizer`** ([agents/visualizer.md](file:///d:/Agent%20SKILLS/ultra-skill/agents/visualizer.md)): Archify interactive architecture diagrams (SVG/HTML), visual QA, and design-to-code synthesis.
- **`@engineer`** ([agents/engineer.md](file:///d:/Agent%20SKILLS/ultra-skill/agents/engineer.md)): Lazy senior engineer mode, YAGNI, standard library first, shortest diff wins.
- **`@designer`** ([agents/designer.md](file:///d:/Agent%20SKILLS/ultra-skill/agents/designer.md)): Anti-slop frontend aesthetics, responsive ladder, 4px grid, dark mode, and contrast locks.
- **`@animator`** ([agents/animator.md](file:///d:/Agent%20SKILLS/ultra-skill/agents/animator.md)): 60fps GPU animations, animation inventory, 3 motion layers, ScrollTrigger cleanup.
- **`@debugger`** ([agents/debugger.md](file:///d:/Agent%20SKILLS/ultra-skill/agents/debugger.md)): 4-phase root-cause investigation, distributed tracing, memory leak forensics, and 3-fix circuit breaker.
- **`@tester`** ([agents/tester.md](file:///d:/Agent%20SKILLS/ultra-skill/agents/tester.md)): Red-Green-Refactor enforcement; coverage targets (80% line, 70% branch) & quarantine protocols.
- **`@reviewer`** ([agents/reviewer.md](file:///d:/Agent%20SKILLS/ultra-skill/agents/reviewer.md)): Autonomous security scan, secret hygiene, dependency audits & license compliance.
- **`@verifier`** ([agents/verifier.md](file:///d:/Agent%20SKILLS/ultra-skill/agents/verifier.md)): Parallel verification matrices, receipt archival (`.verification/`), exit code 0 gate.

---

## 📋 Actionable Workflows Map

- [01: ADK 2.0 Graph & Multi-Agent Orchestration](file:///d:/Agent%20SKILLS/ultra-skill/workflows/01-agent-graph-orchestration.md)
- [02: Subagent-Driven Development & Parallel Dispatch](file:///d:/Agent%20SKILLS/ultra-skill/workflows/02-subagent-driven-development.md)
- [03: Anti-Slop Frontend Design](file:///d:/Agent%20SKILLS/ultra-skill/workflows/03-anti-slop-frontend-design.md)
- [04: Cinematic Motion Choreography & Animation](file:///d:/Agent%20SKILLS/ultra-skill/workflows/04-cinematic-motion-choreography.md)
- [05: Systematic Root-Cause Debugging](file:///d:/Agent%20SKILLS/ultra-skill/workflows/05-systematic-root-cause-debugging.md)
- [06: Test-Driven Development (TDD)](file:///d:/Agent%20SKILLS/ultra-skill/workflows/06-test-driven-development.md)
- [07: Autonomous Code Review & Security Audit](file:///d:/Agent%20SKILLS/ultra-skill/workflows/07-autonomous-code-review.md)
- [08: Design DNA Extraction & Style Transfer](file:///d:/Agent%20SKILLS/ultra-skill/workflows/08-design-dna-extraction.md)
- [09: Brand Asset Production (UI/UX Pro Max)](file:///d:/Agent%20SKILLS/ultra-skill/workflows/09-brand-asset-production.md)
- [10: Gate-Function Verification Before Completion](file:///d:/Agent%20SKILLS/ultra-skill/workflows/10-gate-function-verification.md)
- [11: Interactive Architecture Visualization (Archify)](file:///d:/Agent%20SKILLS/ultra-skill/workflows/11-interactive-architecture-visualization.md)
- [12: Implementation Planning & Progress Checklists](file:///d:/Agent%20SKILLS/ultra-skill/workflows/12-implementation-planning-and-checklists.md)
- [13: Error Recovery & Graceful Degradation](file:///d:/Agent%20SKILLS/ultra-skill/workflows/13-error-recovery-and-graceful-degradation.md)
- [14: Performance Profiling & Optimization](file:///d:/Agent%20SKILLS/ultra-skill/workflows/14-performance-profiling-and-optimization.md)

---

## 🛠️ Verification & Diagnostic Utilities

- **Gate Verification Runner:** `python scripts/verify_evidence.py "<command>"` (supports `--json`, `--save`)
- **AI Slop Detector:** `python scripts/detect_ai_slop.py <path>` (supports `--json`, `--fix`, `.slopignore`)
- **WCAG Contrast Checker:** `python scripts/contrast_checker.py <fg> <bg>` or `<path>` (supports `--json`, `--strict`)
- **Implementation Plan Validator:** `python scripts/plan_validator.py <plan.md>` (supports `--json`, `--strict`)
- **ADK Trace Inspector:** `python scripts/adk_trace_inspector.py <logfile.jsonl>` (supports latency timing & `--filter-tool`)
- **Archify Finalizer:** `node skills/ultra-skill/references/archify/bin/archify.mjs finalize <type> <candidate.json> <output.html>`
