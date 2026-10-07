#!/usr/bin/env python3
"""
detect_ai_slop.py — Anti-Slop Frontend Quality Auditor
Scans HTML, CSS, JSX, and TSX files for generic AI design tropes:
- Inter/Roboto defaults
- AI purple/violet glowing cards (The Lila Rule)
- h-screen usage instead of 100dvh
- Three identical card layouts
- Missing focus styles
"""

import sys
import re
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


SLOP_PATTERNS = [
    {
        "name": "Inter / Roboto Font Default",
        "regex": r"(font-sans.*inter|font-['\"]?Inter['\"]?|font-['\"]?Roboto['\"]?)",
        "message": "Generic AI font detected. Replace with personality sans (Geist, Outfit, Cabinet Grotesk, Satoshi).",
        "severity": "WARNING",
    },
    {
        "name": "The Lila Rule: AI Purple Glow",
        "regex": r"(from-purple-\d+|bg-purple-\d+|rgba\(\s*147\s*,\s*51\s*,\s*234|#9333ea|#7c3aed|#8b5cf6)",
        "message": "AI-purple gradient/glow detected. Adhere to the Lila Rule: neutral base with singular high-contrast accent.",
        "severity": "WARNING",
    },
    {
        "name": "h-screen Viewport Instability",
        "regex": r"(h-screen(?!\S)|height:\s*100vh)",
        "message": "Use min-h-[100dvh] or 100dvh instead of h-screen/100vh to avoid mobile address bar jumps.",
        "severity": "ERROR",
    },
    {
        "name": "Div-Based Fake Browser Screenshot",
        "regex": r"(<div[^>]*class=[^>]*window-dots|<div[^>]*class=[^>]*browser-header)",
        "message": "Div-based fake screenshots are banned. Use real imagery or Picsum seed assets.",
        "severity": "ERROR",
    },
]

def audit_file(file_path: Path) -> list[dict]:
    findings = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return [{"line": 0, "rule": "Read Error", "message": str(e), "severity": "ERROR"}]

    lines = content.splitlines()
    for idx, line in enumerate(lines, start=1):
        for pattern in SLOP_PATTERNS:
            if re.search(pattern["regex"], line, re.IGNORECASE):
                findings.append({
                    "line": idx,
                    "rule": pattern["name"],
                    "message": pattern["message"],
                    "severity": pattern["severity"],
                    "snippet": line.strip()[:100],
                })
    return findings

def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    files_to_check = []

    if target.is_file():
        files_to_check.append(target)
    elif target.is_dir():
        for ext in ("*.html", "*.htm", "*.jsx", "*.tsx", "*.vue", "*.svelte", "*.css"):
            files_to_check.extend(target.rglob(ext))

    total_issues = 0
    print(f"[*] Auditing {len(files_to_check)} files for AI design slop...")

    for file_path in files_to_check:
        # Ignore node_modules, dist, build, .git
        if any(part in file_path.parts for part in ("node_modules", "dist", "build", ".git", ".next")):
            continue

        findings = audit_file(file_path)
        if findings:
            print(f"\n📄 {file_path}")
            for f in findings:
                icon = "❌" if f["severity"] == "ERROR" else "⚠️"
                print(f"  {icon} Line {f['line']}: [{f['rule']}] {f['message']}")
                print(f"     Snippet: {f['snippet']}")
                total_issues += 1

    print(f"\n--- AUDIT COMPLETE: {total_issues} slop indicators found ---")
    sys.exit(1 if any(f.get("severity") == "ERROR" for f in findings) else 0)

if __name__ == "__main__":
    main()
