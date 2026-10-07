# ⚡ Ultra Skill — Universal AI Agent Architecture & Rules

> **Master Directive:** Read and follow [skills/ultra-skill/SKILL.md](file:///d:/Agent%20SKILLS/ultra-skill/skills/ultra-skill/SKILL.md) for every task. Execute via the deterministic 6-phase Agentic State Machine.

---

## 🧭 The 6-Phase Agentic State Machine

1. **State 0: Intake & Intent Routing:** Classify request domain, bind active subagent roles, and map applicable reference manuals.
2. **State 1: Reconnaissance & Fact-Gathering:** Audit code, dependencies, and interfaces before authoring any diff. Formulate Design Read (Frontend) or Trace Log (ADK).
3. **State 2: Contract & Decomposition:** Formulate zero-context implementation specs with atomic TDD task steps.
4. **State 3: Subagent Execution:** Apply Ponytail Ladder (shortest working diff) and Red-Green-Refactor TDD discipline.
5. **State 4: Autonomous Review & Correction:** Run CodeRabbit security scan, classify issues (Critical → Info), and run slop detector.
6. **State 5: Gate-Function Verification:** Execute fresh terminal verification commands. Exit code `0` and zero failures required before claiming completion.

---

## 👥 Subagent Roles & Personas

When executing specialized tasks, assume or dispatch these dedicated subagent roles:
- **`@architect`** ([agents/architect.md](file:///d:/Agent%20SKILLS/ultra-skill/agents/architect.md)): Google ADK 2.0 graphs, dynamic nodes, state channels, and HITL interrupts.
- **`@visualizer`** ([agents/visualizer.md](file:///d:/Agent%20SKILLS/ultra-skill/agents/visualizer.md)): Archify interactive architecture, workflow, sequence, dataflow & lifecycle diagrams (SVG/HTML).
- **`@engineer`** ([agents/engineer.md](file:///d:/Agent%20SKILLS/ultra-skill/agents/engineer.md)): Lazy senior engineer mode, YAGNI, standard library first, shortest diff wins.
- **`@designer`** ([agents/designer.md](file:///d:/Agent%20SKILLS/ultra-skill/agents/designer.md)): Anti-slop frontend aesthetics, 3 dials, layout rules, typography locks, color consistency.
- **`@animator`** ([agents/animator.md](file:///d:/Agent%20SKILLS/ultra-skill/agents/animator.md)): 60fps GPU animations, 3 motion layers, ScrollTrigger, `prefers-reduced-motion`.
- **`@debugger`** ([agents/debugger.md](file:///d:/Agent%20SKILLS/ultra-skill/agents/debugger.md)): 4-phase root-cause investigation, boundary logs, 3-fix circuit breaker.
- **`@tester`** ([agents/tester.md](file:///d:/Agent%20SKILLS/ultra-skill/agents/tester.md)): Red-Green-Refactor enforcement; no production code without failing tests.
- **`@reviewer`** ([agents/reviewer.md](file:///d:/Agent%20SKILLS/ultra-skill/agents/reviewer.md)): Autonomous security scan, secret hygiene, severity classification.
- **`@verifier`** ([agents/verifier.md](file:///d:/Agent%20SKILLS/ultra-skill/agents/verifier.md)): 5-step gate function, command execution verification, exit code 0 assertion.

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

---

## 🛠️ Verification & Diagnostic Utilities

- **Gate Verification Runner:** `python scripts/verify_evidence.py "<command>"`
- **AI Slop Detector:** `python scripts/detect_ai_slop.py <path>`
- **ADK Trace Inspector:** `python scripts/adk_trace_inspector.py <logfile.jsonl>`
- **Archify Finalizer:** `node skills/ultra-skill/references/archify/bin/archify.mjs finalize <type> <candidate.json> <output.html>`
