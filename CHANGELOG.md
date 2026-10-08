# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [4.0.0] - 2026-10-08

### Added
- **Workflow 13 (`workflows/13-error-recovery-and-graceful-degradation.md`):** Systematic multi-tier error handling covering transient tool retries with exponential backoff & jitter, 3-failure circuit breakers, atomic git workspace rollback, and graceful degradation strategies.
- **Workflow 14 (`workflows/14-performance-profiling-and-optimization.md`):** Performance engineering pipeline covering Core Web Vitals (LCP, INP, CLS), bundle analyzer budgets (initial JS $\le 150\text{KB}$), 60fps frame rate budgets, and image/asset optimization.
- **WCAG Contrast Checker Script (`scripts/contrast_checker.py`):** Automated tool calculating relative luminance and contrast ratios per W3C WCAG 2.1 specs; supports hex, rgb, named colors, and batch file scanning with `--json` and `--strict` options.
- **Implementation Plan Validator Script (`scripts/plan_validator.py`):** Schema enforcement tool verifying Goal, Architecture, Tech Stack, Affected Files, Master Checklist, `- [ ]` syntax, disk file existence, and 20-task decomposition ceilings.
- **Automated Script Test Suite (`tests/`):** Comprehensive unit tests covering all 5 scripts (`test_detect_ai_slop.py`, `test_verify_evidence.py`, `test_contrast_checker.py`, `test_plan_validator.py`, and `test_adk_trace_inspector.py`).
- **New Slash Commands:** Added `/recover` (for error recovery and circuit breakers) and `/perf` (for Core Web Vitals and 60fps frame budget profiling).
- **Ecosystem Files:** Added official `LICENSE` (MIT) and enhanced platform entry points (`CLAUDE.md`, `GEMINI.md`).

### Changed
- **Subagent Personas Deepened (`agents/*.md`):** Expanded all 10 agent specifications with formal failure escalation protocols, anti-patterns, context requirements, collaboration interfaces, and output format contracts:
  - `@planner`: Risk tier classification (🔴/🟡/🟢), dependency DAGs, T-shirt sizing, sub-plan splitting.
  - `@architect`: ADK 2.0 graph topologies, retry/backoff strategies, circuit breakers, max 3-tier nesting limit.
  - `@engineer`: 7-rung Ponytail ladder, diff size guardrails (>200 lines / >5 files warning), dependency audits.
  - `@designer`: Mobile-first 6-breakpoint ladder, 4px base spacing grid, dark/light mode protocols, icon sizing rules.
  - `@animator`: 16.67ms frame budgets, animation inventory catalog, 3-tier stagger limits, ScrollTrigger SPA cleanup.
  - `@debugger`: 4-phase debugging, structured JSON logging, distributed tracing correlation, heap memory leak forensics.
  - `@tester`: Quantitative coverage thresholds (80% line, 70% branch), test pyramid ratios, flaky test quarantine.
  - `@reviewer`: Vulnerability scanning (`npm audit`/`pip audit`), license compliance, bundle regression detection.
  - `@verifier`: Parallel gate matrices, receipt archival (`.verification/`), regression guard comparison.
  - `@visualizer`: 4-phase design DNA extraction, visual QA matrix, screenshot verification protocol.
- **Script Hardening:**
  - `scripts/detect_ai_slop.py`: Fixed `UnboundLocalError` on empty scans, added exit code correctness logic, expanded patterns to 9 anti-slop rules, added `--fix` advice, `--json` output, and `.slopignore` support.
  - `scripts/verify_evidence.py`: Added machine-parseable `--json` output, `--save` receipt certificate creation, and configurable `--timeout`.
  - `scripts/adk_trace_inspector.py`: Added tool latency analysis (highlighting calls $\ge 5\text{s}$), token consumption heuristics, `--filter-tool` filtering, and JSON output mode.
- **Workflow Interconnectivity:** Added explicit `## Prerequisites` and `## Related Workflows` cross-references across all 14 workflow guides.
- **Workflow 02 Conflict Resolution:** Added file partition ownership reservations, Git worktree isolation, and 3-way merge conflict resolution for parallel agent dispatches.
- **Module Normalization:** Integrated §12 (Performance Guardrails) and §13 (Accessibility Checklist) into the master modules matrix.

---

## [3.1.0] - 2026-03-15

### Added
- Initial unified orchestration of 11 AI agent systems.
- 10 specialized subagent personas (`agents/`).
- 12 core executable workflows (`workflows/`).
- 3 utility scripts (`scripts/verify_evidence.py`, `scripts/detect_ai_slop.py`, `scripts/adk_trace_inspector.py`).
- Integrated references archives for ADK 2.0, Archify, Superpowers, Taste, Ponytail, GSAP, Motion Design, Design DNA, UI/UX Pro Max, and CodeRabbit.
