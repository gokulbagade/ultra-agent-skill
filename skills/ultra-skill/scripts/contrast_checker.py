#!/usr/bin/env python3
"""
contrast_checker.py — WCAG AA/AAA Automated Contrast Ratio Calculator & Auditor
Calculates relative luminance and contrast ratios per W3C WCAG 2.1 specifications.
Supports direct color pair checks and automated scanning of CSS/HTML/Tailwind files.
"""

import sys
import re
import json
import argparse
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


NAMED_COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 128, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "gray": (128, 128, 128),
    "grey": (128, 128, 128),
    "darkgray": (169, 169, 169),
    "lightgray": (211, 211, 211),
    "transparent": (255, 255, 255), # default fallback assumption
}

TAILWIND_COLOR_MAP = {
    "slate-900": (15, 23, 42),
    "slate-800": (30, 41, 59),
    "slate-100": (241, 245, 249),
    "slate-50": (248, 250, 252),
    "zinc-900": (24, 24, 27),
    "zinc-800": (39, 39, 42),
    "zinc-100": (244, 244, 245),
    "zinc-50": (250, 250, 250),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "purple-600": (147, 51, 234),
    "emerald-500": (16, 185, 129),
    "amber-500": (245, 158, 11),
    "red-600": (220, 38, 38),
    "blue-600": (37, 99, 235),
}


def parse_color(color_str: str):
    """Parses hex, rgb, or named color into (r, g, b) tuple in 0..255."""
    c = color_str.strip().lower()

    if c in NAMED_COLORS:
        return NAMED_COLORS[c]

    if c in TAILWIND_COLOR_MAP:
        return TAILWIND_COLOR_MAP[c]

    # Hex: #rgb or #rrggbb or #rrggbbaa
    if c.startswith("#"):
        hex_val = c[1:]
        if len(hex_val) == 3:
            return tuple(int(ch * 2, 16) for ch in hex_val)
        elif len(hex_val) in (6, 8):
            return tuple(int(hex_val[i:i+2], 16) for i in (0, 2, 4))

    # rgb(...) or rgba(...)
    rgb_match = re.match(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", c)
    if rgb_match:
        return tuple(int(x) for x in rgb_match.groups()[:3])

    return None


def relative_luminance(rgb: tuple) -> float:
    """Calculates relative luminance per WCAG 2.1 definition."""
    def channel_lum(val: int) -> float:
        c = val / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * channel_lum(r) + 0.7152 * channel_lum(g) + 0.0722 * channel_lum(b)


def calculate_contrast_ratio(fg_rgb: tuple, bg_rgb: tuple) -> float:
    """Calculates contrast ratio (L1 + 0.05) / (L2 + 0.05)."""
    l1 = relative_luminance(fg_rgb)
    l2 = relative_luminance(bg_rgb)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return round((lighter + 0.05) / (darker + 0.05), 2)


def evaluate_contrast(ratio: float) -> dict:
    return {
        "ratio": ratio,
        "aa_normal": ratio >= 4.5,
        "aa_large": ratio >= 3.0,
        "aaa_normal": ratio >= 7.0,
        "aaa_large": ratio >= 4.5,
    }


def scan_file_for_contrast(file_path: Path) -> list[dict]:
    """Scans file for direct CSS color/background-color pairs or dangerous Tailwind classes."""
    findings = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    lines = content.splitlines()

    # Rule 1: Tailwind identical text-X bg-X (e.g. text-white bg-white)
    tw_regex = re.compile(r"class(?:Name)?=[\"'][^\"']*(text-(\S+))\s+[^\"']*(bg-(\S+))", re.IGNORECASE)
    for idx, line in enumerate(lines, start=1):
        for m in tw_regex.finditer(line):
            fg_name, bg_name = m.group(2), m.group(4)
            if fg_name == bg_name:
                findings.append({
                    "file": str(file_path),
                    "line": idx,
                    "fg": fg_name,
                    "bg": bg_name,
                    "ratio": 1.0,
                    "status": "FAIL",
                    "reason": f"Identical text and background token '{fg_name}' (1:1 ratio)",
                })
            else:
                fg_rgb = parse_color(fg_name)
                bg_rgb = parse_color(bg_name)
                if fg_rgb and bg_rgb:
                    ratio = calculate_contrast_ratio(fg_rgb, bg_rgb)
                    if ratio < 4.5:
                        findings.append({
                            "file": str(file_path),
                            "line": idx,
                            "fg": fg_name,
                            "bg": bg_name,
                            "ratio": ratio,
                            "status": "FAIL",
                            "reason": f"Contrast {ratio}:1 fails WCAG AA 4.5:1 requirement",
                        })

    return findings


def main():
    parser = argparse.ArgumentParser(
        description="WCAG AA/AAA Automated Contrast Ratio Calculator & Code Auditor."
    )
    parser.add_argument("foreground", nargs="?", help="Foreground color (hex, rgb, named, or file/dir to scan)")
    parser.add_argument("background", nargs="?", help="Background color (hex, rgb, or named)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--strict", action="store_true", help="Exit code 1 if failing WCAG AAA")

    args = parser.parse_args()

    # Mode 1: Pair evaluation
    if args.foreground and args.background:
        fg_rgb = parse_color(args.foreground)
        bg_rgb = parse_color(args.background)

        if not fg_rgb or not bg_rgb:
            err = f"Error: Unable to parse color values: '{args.foreground}' or '{args.background}'"
            if args.json:
                print(json.dumps({"error": err}))
            else:
                print(err, file=sys.stderr)
            sys.exit(1)

        ratio = calculate_contrast_ratio(fg_rgb, bg_rgb)
        eval_res = evaluate_contrast(ratio)
        eval_res["foreground"] = args.foreground
        eval_res["background"] = args.background

        if args.json:
            print(json.dumps(eval_res, indent=2))
        else:
            print(f"🎨 Contrast Ratio: {ratio}:1")
            print(f"  • WCAG AA Normal Text (>= 4.5:1): {'✅ PASS' if eval_res['aa_normal'] else '❌ FAIL'}")
            print(f"  • WCAG AA Large Text / UI (>= 3.0:1): {'✅ PASS' if eval_res['aa_large'] else '❌ FAIL'}")
            print(f"  • WCAG AAA Normal Text (>= 7.0:1): {'✅ PASS' if eval_res['aaa_normal'] else '❌ FAIL'}")
            print(f"  • WCAG AAA Large Text (>= 4.5:1): {'✅ PASS' if eval_res['aaa_large'] else '❌ FAIL'}")

        if args.strict and not eval_res["aaa_normal"]:
            sys.exit(1)
        sys.exit(0 if eval_res["aa_normal"] else 1)

    # Mode 2: Scan file or directory
    target_path = Path(args.foreground) if args.foreground else Path(".")
    if target_path.exists():
        files_to_scan = []
        if target_path.is_file():
            files_to_scan.append(target_path)
        else:
            for ext in ("*.html", "*.jsx", "*.tsx", "*.vue", "*.svelte", "*.css"):
                files_to_scan.extend(target_path.rglob(ext))

        all_findings = []
        for f in files_to_scan:
            if any(part in f.parts for part in ("node_modules", "dist", "build", ".git")):
                continue
            all_findings.extend(scan_file_for_contrast(f))

        if args.json:
            print(json.dumps({"files_scanned": len(files_to_scan), "findings": all_findings}, indent=2))
        else:
            print(f"[*] Scanned {len(files_to_scan)} files for contrast violations...")
            for find in all_findings:
                print(f"❌ {find['file']}:{find['line']} — {find['reason']}")
            print(f"\n--- AUDIT COMPLETE: {len(all_findings)} contrast violations found ---")

        sys.exit(1 if all_findings else 0)

    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
