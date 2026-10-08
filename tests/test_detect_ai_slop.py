#!/usr/bin/env python3
"""
Unit tests for detect_ai_slop.py
"""

import sys
import unittest
import tempfile
from pathlib import Path

# Add scripts directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from detect_ai_slop import audit_file, load_slopignore, is_ignored, SLOP_PATTERNS


class TestDetectAiSlop(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.dir_path = Path(self.test_dir.name)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_clean_file_has_zero_slop(self):
        clean_file = self.dir_path / "clean.html"
        clean_file.write_text("""
        <!DOCTYPE html>
        <html class="font-outfit">
        <body class="min-h-[100dvh] bg-slate-900 text-slate-100">
            <h1 class="text-4xl font-bold">Clean Modern Interface</h1>
            <a href="/pricing" class="px-4 py-2 bg-emerald-500 text-black">Explore Pricing</a>
        </body>
        </html>
        """, encoding="utf-8")

        findings = audit_file(clean_file)
        self.assertEqual(len(findings), 0)

    def test_detects_inter_font_default(self):
        slop_file = self.dir_path / "inter.html"
        slop_file.write_text('<body class="font-sans font-inter text-white">', encoding="utf-8")

        findings = audit_file(slop_file)
        self.assertTrue(any("Inter / Roboto" in f["rule"] for f in findings))

    def test_detects_lila_purple_glow(self):
        slop_file = self.dir_path / "purple.html"
        slop_file.write_text('<div class="bg-purple-600 shadow-lg shadow-purple-500/50">', encoding="utf-8")

        findings = audit_file(slop_file)
        self.assertTrue(any("Lila Rule" in f["rule"] for f in findings))

    def test_detects_h_screen_instability(self):
        slop_file = self.dir_path / "screen.html"
        slop_file.write_text('<main class="h-screen w-full">', encoding="utf-8")

        findings = audit_file(slop_file)
        self.assertTrue(any("h-screen" in f["rule"] for f in findings))
        error_finding = next(f for f in findings if "h-screen" in f["rule"])
        self.assertEqual(error_finding["severity"], "ERROR")

    def test_detects_lorem_ipsum(self):
        slop_file = self.dir_path / "lorem.html"
        slop_file.write_text('<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>', encoding="utf-8")

        findings = audit_file(slop_file)
        self.assertTrue(any("Lorem Ipsum" in f["rule"] for f in findings))

    def test_detects_white_on_white_cta(self):
        slop_file = self.dir_path / "cta.html"
        slop_file.write_text('<button class="px-4 py-2 bg-white text-white font-bold">Submit</button>', encoding="utf-8")

        findings = audit_file(slop_file)
        self.assertTrue(any("White-on-White" in f["rule"] for f in findings))

    def test_slopignore_loads_and_filters(self):
        ignore_file = self.dir_path / ".slopignore"
        ignore_file.write_text("vendor/*\nlegacy.html\n# comment\n", encoding="utf-8")

        patterns = load_slopignore(ignore_file)
        self.assertEqual(patterns, ["vendor/*", "legacy.html"])

        self.assertTrue(is_ignored(Path("src/vendor/bundle.js"), patterns))
        self.assertTrue(is_ignored(Path("legacy.html"), patterns))
        self.assertFalse(is_ignored(Path("src/app.tsx"), patterns))


if __name__ == "__main__":
    unittest.main()
