#!/usr/bin/env python3
"""
Unit tests for adk_trace_inspector.py
"""

import sys
import unittest
import io
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from adk_trace_inspector import inspect_stream, estimate_tokens


class TestAdkTraceInspector(unittest.TestCase):
    def test_estimate_tokens(self):
        text = "This is a simple sample string for testing."
        tokens = estimate_tokens(text)
        self.assertGreater(tokens, 0)
        self.assertEqual(tokens, len(text) // 4)

    def test_inspect_clean_stream(self):
        events = [
            json.dumps({"event_type": "node_start", "name": "router"}),
            json.dumps({"event_type": "tool_call", "name": "search_db", "args": {"q": "test"}, "duration": 0.45}),
            json.dumps({"event_type": "node_end", "name": "router", "route": "success"}),
        ]
        stream = io.StringIO("\n".join(events))
        exit_code = inspect_stream(stream, as_json=True)
        self.assertEqual(exit_code, 0)

    def test_inspect_error_stream(self):
        events = [
            json.dumps({"event_type": "node_start", "name": "step1"}),
            json.dumps({"event_type": "error", "message": "Connection refused", "status": "error"}),
        ]
        stream = io.StringIO("\n".join(events))
        exit_code = inspect_stream(stream, as_json=True)
        self.assertEqual(exit_code, 1)

    def test_slow_tool_call_flagged(self):
        events = [
            json.dumps({"event_type": "tool_call", "name": "slow_external_api", "duration": 8.2}),
        ]
        stream = io.StringIO("\n".join(events))
        # inspect_stream prints slow tools or includes in output
        # capturing stdout to verify warning
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            inspect_stream(stream, warn_duration=5.0, as_json=False)
            output = sys.stdout.getvalue()
            self.assertIn("High-Latency Tool Calls", output)
            self.assertIn("slow_external_api", output)
        finally:
            sys.stdout = old_stdout


if __name__ == "__main__":
    unittest.main()
