#!/usr/bin/env python3
"""
Unit tests for verify_evidence.py
"""

import sys
import unittest
import tempfile
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from verify_evidence import run_verification


class TestVerifyEvidence(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.dir_path = Path(self.test_dir.name)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_successful_command_passes(self):
        result = run_verification('echo "hello world"')
        self.assertTrue(result["passed"])
        self.assertEqual(result["exit_code"], 0)
        self.assertIn("hello world", result["stdout"])
        self.assertIsNone(result["error_message"])

    def test_failed_command_fails(self):
        # Use sys.executable to ensure we use the active Python binary
        result = run_verification(f'"{sys.executable}" -c "import sys; sys.exit(1)"')
        self.assertFalse(result["passed"])
        self.assertEqual(result["exit_code"], 1)

    def test_command_duration_recorded(self):
        result = run_verification('echo "timing test"')
        self.assertIsInstance(result["duration_seconds"], float)
        self.assertGreaterEqual(result["duration_seconds"], 0.0)

    def test_save_receipt_creates_valid_json(self):
        result = run_verification('echo "receipt test"')
        receipt_file = self.dir_path / ".verification" / "receipt.json"
        receipt_file.parent.mkdir(parents=True, exist_ok=True)
        receipt_file.write_text(json.dumps(result, indent=2), encoding="utf-8")

        self.assertTrue(receipt_file.exists())
        data = json.loads(receipt_file.read_text(encoding="utf-8"))
        self.assertEqual(data["command"], 'echo "receipt test"')
        self.assertTrue(data["passed"])


if __name__ == "__main__":
    unittest.main()
