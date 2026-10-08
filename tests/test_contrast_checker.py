#!/usr/bin/env python3
"""
Unit tests for contrast_checker.py
"""

import sys
import unittest
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from contrast_checker import (
    parse_color,
    relative_luminance,
    calculate_contrast_ratio,
    evaluate_contrast,
    scan_file_for_contrast,
)


class TestContrastChecker(unittest.TestCase):
    def test_parse_hex_colors(self):
        self.assertEqual(parse_color("#fff"), (255, 255, 255))
        self.assertEqual(parse_color("#ffffff"), (255, 255, 255))
        self.assertEqual(parse_color("#000000"), (0, 0, 0))
        self.assertEqual(parse_color("#ff0000"), (255, 0, 0))

    def test_parse_named_and_tailwind_colors(self):
        self.assertEqual(parse_color("white"), (255, 255, 255))
        self.assertEqual(parse_color("black"), (0, 0, 0))
        self.assertEqual(parse_color("slate-900"), (15, 23, 42))

    def test_black_white_contrast_ratio(self):
        white = (255, 255, 255)
        black = (0, 0, 0)
        ratio = calculate_contrast_ratio(white, black)
        self.assertEqual(ratio, 21.0)

        eval_res = evaluate_contrast(ratio)
        self.assertTrue(eval_res["aa_normal"])
        self.assertTrue(eval_res["aa_large"])
        self.assertTrue(eval_res["aaa_normal"])
        self.assertTrue(eval_res["aaa_large"])

    def test_low_contrast_fails_aa(self):
        gray1 = (130, 130, 130)
        gray2 = (140, 140, 140)
        ratio = calculate_contrast_ratio(gray1, gray2)
        eval_res = evaluate_contrast(ratio)
        self.assertFalse(eval_res["aa_normal"])
        self.assertFalse(eval_res["aa_large"])

    def test_scan_file_detects_identical_tokens(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            f = Path(tmp_dir) / "test.html"
            f.write_text('<button class="px-4 py-2 text-white bg-white font-bold">Invisible</button>', encoding="utf-8")

            findings = scan_file_for_contrast(f)
            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0]["status"], "FAIL")
            self.assertEqual(findings[0]["ratio"], 1.0)


if __name__ == "__main__":
    unittest.main()
