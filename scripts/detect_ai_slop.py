#!/usr/bin/env python3
"""
detect_ai_slop.py — Anti-Slop Frontend Quality Auditor
Scans HTML, CSS, JSX, TSX, Vue, and Svelte files for generic AI design tropes:
- Inter/Roboto defaults
- AI purple/violet glowing cards (The Lila Rule)
- h-screen/100vh usage instead of 100dvh
- Div-based fake browser mockups
- Lorem ipsum placeholder text
- White-on-white / unreadable low-contrast CTAs
- Serif injection / generic typography
- Three identical cards pattern
- Missing prefers-reduced-motion in animations
- Generic anchor copy ("click here", "learn more")
"""

import sys
import os
import re
import json
import argparse
import fnmatch
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
        "regex": r"(font-sans.*inter|font-['\"]?Inter['\"]?|font-['\"]?Roboto['\"]?|font-family:\s*[^;]*(?:['\"]?Inter['\"]?|['\"]?Roboto['\"]))",
        "message": "Generic AI font default detected. Replace with personality sans (Geist, Outfit, Cabinet Grotesk, Satoshi, Plus Jakarta Sans).",
        "fix": "Replace font family with 'Geist', 'Outfit', or 'Cabinet Grotesk'.",
        "severity": "WARNING",
    },
    {
        "name": "The Lila Rule: AI Purple Glow",
        "regex": r"(from-purple-\d+|bg-purple-\d+|to-purple-\d+|border-purple-\d+|rgba\(\s*147\s*,\s*51\s*,\s*234|#9333ea|#7c3aed|#8b5cf6|#a855f7|violet-600|purple-600)",
        "message": "AI-purple gradient/glow detected. Adhere to the Lila Rule: neutral dark/light base with singular purposeful accent.",
        "fix": "Switch to neutral slate/zinc base with high-contrast accent (e.g. emerald, amber, or international orange).",
        "severity": "WARNING",
    },
    {
        "name": "h-screen Viewport Instability",
        "regex": r"(\bh-screen\b|height:\s*100vh\b)",
        "message": "Use min-h-[100dvh] or 100dvh instead of h-screen/100vh to prevent mobile address bar jump jitter.",
        "fix": "Replace h-screen with min-h-[100dvh] or height: 100dvh.",
        "severity": "ERROR",
    },
    {
        "name": "Div-Based Fake Browser Screenshot",
        "regex": r"(<div[^>]*class=[^>]*(?:window-dots|browser-header|mockup-browser))",
        "message": "Div-based fake screenshots with window dots are banned. Use authentic product screenshots or curated image assets.",
        "fix": "Replace CSS fake window dots with an <img> or <picture> element containing real app imagery.",
        "severity": "ERROR",
    },
    {
        "name": "Lorem Ipsum Placeholder Text",
        "regex": r"\b(lorem\s+ipsum|dolor\s+sit\s+amet|consectetur\s+adipiscing|sed\s+do\s+eiusmod)\b",
        "message": "Lorem ipsum placeholder copy detected. Use realistic, domain-specific seed copy representing user workflows.",
        "fix": "Replace with domain-specific realistic content (e.g. real user names, real telemetry metrics, real product descriptions).",
        "severity": "ERROR",
    },
    {
        "name": "White-on-White / Inverted CTA Contrast Hazard",
        "regex": r"(bg-white\s+text-white|bg-black\s+text-black|text-white\s+bg-white|border-white\s+text-white\s+bg-transparent(?![^>]*bg-))",
        "message": "Invisible or high-risk low-contrast CTA combination detected.",
        "fix": "Ensure button text and background maintain minimum 4.5:1 WCAG contrast ratio.",
        "severity": "ERROR",
    },
    {
        "name": "Generic Serif Fallback Injection",
        "regex": r"(font-['\"]?(?:Fraunces|Instrument\s*Serif|Times\s*New\s*Roman)['\"]?)",
        "message": "Default AI serif injection detected. Ensure typography reflects deliberate brand hierarchy, not arbitrary serif pairing.",
        "fix": "Use deliberate typography hierarchy aligned with project design tokens.",
        "severity": "WARNING",
    },
    {
        "name": "Three Identical Cards Pattern",
        "regex": r"(grid-cols-3(?!\S)|repeat\(3,\s*minmax\(0,\s*1fr\)\))",
        "message": "Three equal-width cards detected (standard AI landing page trope). Break monotony with asymmetric grids (2+1 or Bento layout).",
        "fix": "Adopt Bento grid layout or feature spotlight hierarchy instead of three identical cards.",
        "severity": "WARNING",
    },
    {
        "name": "Generic Low-Context Anchor Copy",
        "regex": r"<a[^>]*>\s*(?:click here|learn more|read more)\s*</a>",
        "message": "Generic link text ('click here', 'learn more') fails accessibility guidelines. Use descriptive action labels.",
        "fix": "Use descriptive anchor text like 'Explore Enterprise Pricing' or 'Read the Architecture Guide'.",
        "severity": "WARNING",
    },
]

SEVERITY_LEVELS = {
    "INFO": 1,
    "WARNING": 2,
    "ERROR": 3,
}


def load_slopignore(ignore_path: Path) -> list[str]:
    patterns = []
    if ignore_path.exists():
        try:
            for line in ignore_path.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
        except Exception:
            pass
    return patterns


def is_ignored(file_path: Path, ignore_patterns: list[str]) -> bool:
    norm_path = file_path.as_posix()
    for pattern in ignore_patterns:
        if pattern.endswith("/"):
            if pattern.rstrip("/") in norm_path.split("/"):
                return True
        elif fnmatch.fnmatch(norm_path, f"*{pattern}*") or fnmatch.fnmatch(file_path.name, pattern):
            return True
    return False


def audit_file(file_path: Path, min_severity: str = "WARNING", suggest_fix: bool = False) -> list[dict]:
    findings = []
    min_lvl = SEVERITY_LEVELS.get(min_severity.upper(), 2)

    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return [{
            "file": str(file_path),
            "line": 0,
            "rule": "Read Error",
            "message": str(e),
            "severity": "ERROR",
            "snippet": "",
            "fix": "",
        }]

    lines = content.splitlines()
    for idx, line in enumerate(lines, start=1):
        for pattern in SLOP_PATTERNS:
            if SEVERITY_LEVELS.get(pattern["severity"], 1) < min_lvl:
                continue
            if re.search(pattern["regex"], line, re.IGNORECASE):
                finding = {
                    "file": str(file_path),
                    "line": idx,
                    "rule": pattern["name"],
                    "message": pattern["message"],
                    "severity": pattern["severity"],
                    "snippet": line.strip()[:120],
                }
                if suggest_fix:
                    finding["fix"] = pattern["fix"]
                findings.append(finding)

    # File-level check: Animations without prefers-reduced-motion
    if file_path.suffix in (".css", ".scss", ".less"):
        has_animation = bool(re.search(r"(@keyframes|\banimation\s*:)", content, re.IGNORECASE))
        has_reduced_motion = bool(re.search(r"prefers-reduced-motion", content, re.IGNORECASE))
        if has_animation and not has_reduced_motion and min_lvl <= SEVERITY_LEVELS["WARNING"]:
            finding = {
                "file": str(file_path),
                "line": 1,
                "rule": "Missing prefers-reduced-motion",
                "message": "CSS contains animations but no @media (prefers-reduced-motion) media query override.",
                "severity": "WARNING",
                "snippet": "File-level animation rule",
            }
            if suggest_fix:
                finding["fix"] = "Add @media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }"
            findings.append(finding)

    return findings


def main():
    parser = argparse.ArgumentParser(description="Audit frontend files for AI design slop.")
    parser.add_argument("target", nargs="?", default=".", help="File or directory to audit (default: current directory)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--fix", action="store_true", help="Include actionable fix suggestions")
    parser.add_argument("--min-severity", choices=["INFO", "WARNING", "ERROR"], default="WARNING", help="Minimum severity threshold")
    parser.add_argument("--strict", action="store_true", help="Fail with exit code 1 on any warning or error")
    parser.add_argument("--ignore-file", default=".slopignore", help="Path to ignore file (default: .slopignore)")

    args = parser.parse_args()
    target = Path(args.target)

    # Load ignore patterns
    ignore_path = Path(args.ignore_file)
    if not ignore_path.exists() and (target / ".slopignore").exists():
        ignore_path = target / ".slopignore"
    ignore_patterns = load_slopignore(ignore_path)

    files_to_check = []
    if target.is_file():
        files_to_check.append(target)
    elif target.is_dir():
        for ext in ("*.html", "*.htm", "*.jsx", "*.tsx", "*.vue", "*.svelte", "*.css", "*.scss"):
            files_to_check.extend(target.rglob(ext))
    else:
        print(f"Error: Target '{target}' does not exist.", file=sys.stderr)
        sys.exit(1)

    all_findings = []
    error_count = 0
    warning_count = 0

    for file_path in files_to_check:
        # Standard build/vcs ignore
        parts = file_path.parts
        if any(part in parts for part in ("node_modules", "dist", "build", ".git", ".next", ".turbo", "coverage")):
            continue
        if is_ignored(file_path, ignore_patterns):
            continue

        file_findings = audit_file(file_path, min_severity=args.min_severity, suggest_fix=args.fix)
        for f in file_findings:
            all_findings.append(f)
            if f["severity"] == "ERROR":
                error_count += 1
            elif f["severity"] == "WARNING":
                warning_count += 1

    total_issues = len(all_findings)

    if args.json:
        output_data = {
            "target": str(target),
            "files_scanned": len(files_to_check),
            "total_issues": total_issues,
            "errors": error_count,
            "warnings": warning_count,
            "findings": all_findings,
        }
        print(json.dumps(output_data, indent=2))
    else:
        print(f"[*] Audited {len(files_to_check)} files for AI design slop...")
        current_file = None
        for f in all_findings:
            if f["file"] != current_file:
                current_file = f["file"]
                print(f"\n📄 {current_file}")
            icon = "❌" if f["severity"] == "ERROR" else "⚠️"
            print(f"  {icon} Line {f['line']}: [{f['rule']}] {f['message']}")
            if f.get("snippet"):
                print(f"     Snippet: {f['snippet']}")
            if args.fix and f.get("fix"):
                print(f"     💡 Fix: {f['fix']}")

        print(f"\n--- AUDIT COMPLETE: {total_issues} slop indicators found ({error_count} errors, {warning_count} warnings) ---")

    if args.strict:
        sys.exit(1 if total_issues > 0 else 0)
    else:
        sys.exit(1 if error_count > 0 else 0)


if __name__ == "__main__":
    main()
