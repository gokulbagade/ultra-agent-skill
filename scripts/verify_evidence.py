#!/usr/bin/env python3
"""
verify_evidence.py — Automated Gate-Function Verification Runner
Executes a verification command, checks exit code, scans for failures,
and produces a structured verification certificate.
"""

import sys
import subprocess
import json
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def run_verification(command: str) -> dict:
    start_time = time.time()
    result = {
        "command": command,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "exit_code": 1,
        "duration_seconds": 0.0,
        "passed": False,
        "stdout": "",
        "stderr": "",
        "error_message": None,
    }

    try:
        proc = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300,
        )
        duration = round(time.time() - start_time, 2)
        result["duration_seconds"] = duration
        result["exit_code"] = proc.returncode
        result["stdout"] = proc.stdout.strip()
        result["stderr"] = proc.stderr.strip()
        result["passed"] = proc.returncode == 0

    except subprocess.TimeoutExpired:
        result["duration_seconds"] = round(time.time() - start_time, 2)
        result["error_message"] = "Verification command timed out after 300 seconds."
    except Exception as e:
        result["duration_seconds"] = round(time.time() - start_time, 2)
        result["error_message"] = str(e)

    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_evidence.py <command_to_verify>")
        sys.exit(1)

    cmd = " ".join(sys.argv[1:])
    print(f"[*] Running Gate Verification: '{cmd}'")
    report = run_verification(cmd)

    print("\n--- GATE VERIFICATION RESULT ---")
    if report["passed"]:
        print(f"✅ PASSED (Exit Code: {report['exit_code']}, Duration: {report['duration_seconds']}s)")
        if report["stdout"]:
            print(f"Output:\n{report['stdout']}")
        sys.exit(0)
    else:
        print(f"❌ FAILED (Exit Code: {report['exit_code']}, Duration: {report['duration_seconds']}s)")
        if report["stderr"]:
            print(f"Error:\n{report['stderr']}")
        elif report["stdout"]:
            print(f"Output:\n{report['stdout']}")
        if report.get("error_message"):
            print(f"Details: {report['error_message']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
