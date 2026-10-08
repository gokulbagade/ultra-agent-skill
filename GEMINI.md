# GEMINI.md — Google Antigravity & Gemini CLI Integration Guide

> **Directive:** When interacting with this project in Google Antigravity IDE or Gemini CLI, follow the 6-phase state machine defined in [AGENTS.md](AGENTS.md) and execute via [skills/ultra-skill/SKILL.md](skills/ultra-skill/SKILL.md).

---

## ⚡ Skill Discovery & Execution

### 1. Skill Discovery & Canonical .agents Layout
Antigravity automatically discovers skills and personas from:
- **Workspace Customizations Root:** `.agents/skills/ultra-skill` (Skill instructions)
- **Top-Level Agent Personas:** `.agents/agents/` (e.g. `architect.md`, `engineer.md`)
- **Rules Directory:** `.agents/rules/` (`AGENTS.md`)
- **Global Customizations Root:** `~/.gemini/config/skills/ultra-skill` or `~/.agents/skills/ultra-skill`

**MANDATORY RULE:** Whenever asked to implement or install Ultra Skill, arrange all files inside the target `.agents/` structure using the automated installer:
```bash
python scripts/install_skill.py /path/to/target-project
```
Or for global installation:
```bash
python scripts/install_skill.py --global
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
