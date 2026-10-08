#!/usr/bin/env python3
"""
install_skill.py — Automated Ultra Skill Workspace Installer & Arranger
Installs and arranges Ultra Skill properly inside the target project's `.agents` directory:
- .agents/skills/ultra-skill/  (Self-contained bundle: SKILL.md, agents/, workflows/, scripts/, references/)
- .agents/agents/              (Direct IDE subagent personas: planner.md, architect.md, etc.)
- .agents/rules/               (Rules: AGENTS.md)
- Project root                 (AGENTS.md, CLAUDE.md, GEMINI.md, .slopignore)
"""

import sys
import os
import re
import shutil
import json
import argparse
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


SOURCE_ROOT = Path(__file__).resolve().parent.parent


def copy_directory(src: Path, dst: Path, ignore_patterns=None):
    """Copies directory tree recursively, creating parents if needed."""
    dst.mkdir(parents=True, exist_ok=True)
    if ignore_patterns is None:
        ignore_patterns = shutil.ignore_patterns(
            "__pycache__", "*.pyc", ".git", ".pytest_cache", "node_modules", "dist", "build", ".verification"
        )
    shutil.copytree(src, dst, dirs_exist_ok=True, ignore=ignore_patterns)


def copy_file(src: Path, dst: Path, force: bool = False) -> bool:
    """Copies file if source exists and destination doesn't exist (unless force=True)."""
    if not src.exists():
        return False
    if dst.exists() and not force:
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def adapt_workspace_entrypoints(content: str) -> str:
    """Adapts root entrypoint documentation to reference the target project's .agents directory."""
    # Ensure any previous hardcoded absolute paths are removed
    content = content.replace("file:///d:/Agent%20SKILLS/ultra-skill/", "")
    
    # Use negative lookbehind to avoid duplicate prefixes
    content = re.sub(r'(?<![.\w/])skills/ultra-skill/', '.agents/skills/ultra-skill/', content)
    content = re.sub(r'(?<![.\w/])agents/', '.agents/agents/', content)
    content = re.sub(r'(?<![.\w/])scripts/', '.agents/skills/ultra-skill/scripts/', content)
    content = re.sub(r'(?<![.\w/])workflows/', '.agents/skills/ultra-skill/workflows/', content)
    return content


def clean_loose_root_folders(target_dir: Path) -> list:
    """Cleans up loose root folders (skills, agents, workflows, scripts, tests) if target is not SOURCE_ROOT."""
    cleaned = []
    if target_dir.resolve() == SOURCE_ROOT.resolve():
        return cleaned

    for folder_name in ("skills", "agents", "workflows", "scripts", "tests"):
        loose_dir = target_dir / folder_name
        if loose_dir.exists() and loose_dir.is_dir():
            shutil.rmtree(loose_dir, ignore_errors=True)
            cleaned.append(str(loose_dir))
    return cleaned


def install_ultra_skill(
    target_dir: Path, force: bool = False, as_global: bool = False, clean_root: bool = False
) -> dict:
    """Installs and properly arranges Ultra Skill in target project or global config."""
    result = {
        "target_directory": str(target_dir),
        "status": "FAILED",
        "created_paths": [],
        "cleaned_paths": [],
        "errors": [],
    }

    if not target_dir.exists():
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            result["errors"].append(f"Failed to create target directory: {e}")
            return result

    # Determine base customization root
    if as_global:
        agents_root = target_dir
    else:
        agents_root = target_dir / ".agents"

    skills_dir = agents_root / "skills" / "ultra-skill"
    agents_dir = agents_root / "agents"
    rules_dir = agents_root / "rules"

    try:
        # 1. Arrange .agents/skills/ultra-skill/ (Self-contained skill bundle)
        skills_dir.mkdir(parents=True, exist_ok=True)

        # Copy SKILL.md
        src_skill = SOURCE_ROOT / "skills" / "ultra-skill" / "SKILL.md"
        if not src_skill.exists():
            src_skill = SOURCE_ROOT / "SKILL.md"
        shutil.copy2(src_skill, skills_dir / "SKILL.md")
        result["created_paths"].append(str(skills_dir / "SKILL.md"))

        # Copy agents/, workflows/, scripts/, references/ into skill bundle
        for subfolder in ("agents", "workflows", "scripts", "references"):
            src_sub = SOURCE_ROOT / subfolder
            if not src_sub.exists():
                src_sub = SOURCE_ROOT / "skills" / "ultra-skill" / subfolder
            if src_sub.exists():
                dst_sub = skills_dir / subfolder
                copy_directory(src_sub, dst_sub)
                result["created_paths"].append(str(dst_sub))

        # 2. Arrange .agents/agents/ (Top-level subagent personas for direct discovery)
        agents_dir.mkdir(parents=True, exist_ok=True)
        src_agents = SOURCE_ROOT / "agents"
        if not src_agents.exists():
            src_agents = SOURCE_ROOT / "skills" / "ultra-skill" / "agents"
        if src_agents.exists():
            copy_directory(src_agents, agents_dir)
            result["created_paths"].append(str(agents_dir))

        # 3. Arrange .agents/rules/
        rules_dir.mkdir(parents=True, exist_ok=True)
        src_agents_md = SOURCE_ROOT / "AGENTS.md"
        if src_agents_md.exists():
            content = src_agents_md.read_text(encoding="utf-8")
            if not as_global:
                content = adapt_workspace_entrypoints(content)
            (rules_dir / "AGENTS.md").write_text(content, encoding="utf-8")
            result["created_paths"].append(str(rules_dir / "AGENTS.md"))

        # 4. Project root entrypoints (only for workspace installs)
        if not as_global:
            for root_file in ("AGENTS.md", "CLAUDE.md", "GEMINI.md", ".slopignore"):
                src_file = SOURCE_ROOT / root_file
                dst_file = target_dir / root_file
                if src_file.exists():
                    if dst_file.exists() and not force:
                        continue
                    if root_file.endswith(".md"):
                        content = src_file.read_text(encoding="utf-8")
                        content = adapt_workspace_entrypoints(content)
                        dst_file.write_text(content, encoding="utf-8")
                    else:
                        shutil.copy2(src_file, dst_file)
                    result["created_paths"].append(str(dst_file))

        # 5. Clean up loose root folders if requested
        if clean_root and not as_global:
            cleaned = clean_loose_root_folders(target_dir)
            result["cleaned_paths"] = cleaned

        result["status"] = "SUCCESS"

    except Exception as e:
        result["errors"].append(str(e))
        result["status"] = "ERROR"

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Properly install and arrange Ultra Skill inside the target project's .agents folder."
    )
    parser.add_argument("target_dir", nargs="?", default=".", help="Target project root directory (default: current directory)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files in target directory")
    parser.add_argument("--global", dest="as_global", action="store_true", help="Install into global config root (e.g. ~/.gemini/config or ~/.agents)")
    parser.add_argument("--clean-root", action="store_true", help="Remove redundant loose root folders (skills, agents, workflows, scripts) from target project")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()
    target_path = Path(args.target_dir).resolve()

    res = install_ultra_skill(target_path, force=args.force, as_global=args.as_global, clean_root=args.clean_root)

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        if res["status"] == "SUCCESS":
            print(f"✅ Ultra Skill successfully arranged in: {target_path}")
            print("\n📁 Arranged Structure:")
            print(f"  ├── .agents/skills/ultra-skill/ (SKILL.md, agents/, workflows/, scripts/, references/)")
            print(f"  ├── .agents/agents/            (10 subagent personas)")
            print(f"  ├── .agents/rules/             (AGENTS.md)")
            print(f"  ├── AGENTS.md                  (Universal agent behaviors -> .agents/skills/ultra-skill/SKILL.md)")
            print(f"  ├── CLAUDE.md                  (Claude Code entrypoint)")
            print(f"  ├── GEMINI.md                  (Gemini CLI / Antigravity entrypoint)")
            print(f"  └── .slopignore                (Anti-slop whitelist)")
            if res.get("cleaned_paths"):
                print(f"\n🧹 Cleaned loose root folders:")
                for p in res["cleaned_paths"]:
                    print(f"  - {p}")
        else:
            print(f"❌ Installation failed:", file=sys.stderr)
            for err in res["errors"]:
                print(f"  • {err}", file=sys.stderr)

    sys.exit(0 if res["status"] == "SUCCESS" else 1)


if __name__ == "__main__":
    main()
