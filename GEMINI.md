# GEMINI.md — Google Antigravity & Gemini CLI Integration Guide

> **Directive:** When interacting with this project in Google Antigravity IDE or Gemini CLI, follow the 6-phase state machine defined in [AGENTS.md](file:///d:/Agent%20SKILLS/ultra-skill/AGENTS.md) and execute via [skills/ultra-skill/SKILL.md](file:///d:/Agent%20SKILLS/ultra-skill/skills/ultra-skill/SKILL.md).

---

## ⚡ Skill Discovery & Execution

### 1. Skill Discovery Paths
Antigravity automatically discovers skills from:
- **Workspace Customizations Root:** `.agents/skills/ultra-skill`
- **Global Customizations Root:** `~/.gemini/config/skills/ultra-skill` or `~/.agents/skills/ultra-skill`

To register Ultra Skill in a target project:
```bash
# Windows PowerShell
New-Item -ItemType Directory -Force -Path "$HOME\.agents\skills"
Copy-Item -Recurse -Force "d:\Agent SKILLS\ultra-skill\skills\ultra-skill" "$HOME\.agents\skills\ultra-skill"
```

### 2. State Machine Adherence
1. **State 0: Intake & Routing** — Match prompt to slash command (`/plan`, `/agent`, `/design`, `/debug`, `/recover`, `/perf`).
2. **State 1: Reconnaissance** — Run headless inspection and check current codebase state.
3. **State 2: Mandatory Planning** — Draft implementation plan, validate with `python scripts/plan_validator.py`, build `- [ ]` checklist.
4. **State 3: Execution Loop** — Dispatch personas (`@engineer`, `@designer`, etc.), enforce TDD and Ponytail ladder.
5. **State 4: Review & Correction** — Run `python scripts/detect_ai_slop.py` and `python scripts/contrast_checker.py`.
6. **State 5: Gate Verification** — Execute `python scripts/verify_evidence.py "<command>"` and save receipt before finishing.

### 3. Tool Calling & Headless Diagnostics
- When running ADK 2.0 agents, inspect event streams with:
  ```bash
  adk run --jsonl my_agent "Task" | python scripts/adk_trace_inspector.py
  ```
- All completion claims MUST be verified with exit code `0`.
