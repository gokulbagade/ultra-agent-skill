# CLAUDE.md — Claude Code Integration Guide

> **Directive:** When interacting with this project in Claude Code, read and follow [AGENTS.md](file:///d:/Agent%20SKILLS/ultra-skill/AGENTS.md) and [skills/ultra-skill/SKILL.md](file:///d:/Agent%20SKILLS/ultra-skill/skills/ultra-skill/SKILL.md).

---

## ⚡ Skill Loading & Execution in Claude Code

### 1. Master Rule: The Iron Law of Planning
Never write code or modify files without first authoring an implementation plan and progress checklist (`- [ ]`).
Validate all plans with:
```bash
python scripts/plan_validator.py <plan.md> --workspace .
```

### 2. Subagent Personas
When assuming specialized tasks, adopt the subagent personas in `agents/`:
- `@planner`: Implementation planning, dependency DAGs, atomic checklists.
- `@architect`: ADK 2.0 multi-agent graphs, dynamic nodes, resilience.
- `@visualizer`: Archify interactive HTML system and workflow diagrams.
- `@engineer`: Ponytail lazy engineering (shortest working diff, standard library first).
- `@designer`: Taste anti-slop frontend design, 6-step responsive ladder, WCAG contrast.
- `@animator`: GSAP 60fps frame budgets, animation inventory, reduced motion.
- `@debugger`: 4-phase root-cause investigation, structured logging, 3-fix circuit breaker.
- `@tester`: Red-Green-Refactor TDD discipline, coverage targets (80% line, 70% branch).
- `@reviewer`: Automated code review, security audits, dependency CVE checks.
- `@verifier`: Gatekeeper verification, exit code 0 evidence receipts.

### 3. Verification & Quality Commands
Always verify changes before marking tasks complete:
```bash
# Gate verification runner (captures evidence receipt)
python scripts/verify_evidence.py "pytest tests/"

# Frontend anti-slop audit
python scripts/detect_ai_slop.py ./src --fix

# WCAG contrast ratio audit
python scripts/contrast_checker.py "#ffffff" "#0f172a"
```

### 4. Error Recovery (Workflow 13)
If a tool or operation fails 3 consecutive times, trip the circuit breaker. Do not make a 4th blind attempt. Clean workspace with `git checkout -- .` and present options to the user.
