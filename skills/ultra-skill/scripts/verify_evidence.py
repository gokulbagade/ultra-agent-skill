#!/usr/bin/env python3
"""
verify_evidence.py — Automated Gate-Function Verification Runner
Executes a verification command, checks exit code, scans for failures,
and produces a structured verification certificate.
Supports human-readable terminal output and machine-parseable JSON.
"""

import sys
import subprocess
import json
import time
import argparse
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def run_verification(command: str, timeout: int = 300) -> dict:
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
            timeout=timeout,
        )
        duration = round(time.time() - start_time, 2)
        result["duration_seconds"] = duration
        result["exit_code"] = proc.returncode
        result["stdout"] = proc.stdout.strip()
        result["stderr"] = proc.stderr.strip()
        result["passed"] = (proc.returncode == 0)

    except subprocess.TimeoutExpired:
        result["duration_seconds"] = round(time.time() - start_time, 2)
        result["error_message"] = f"Verification command timed out after {timeout} seconds."
    except Exception as e:
        result["duration_seconds"] = round(time.time() - start_time, 2)
        result["error_message"] = str(e)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Run gate-function verification commands and produce verification receipts.",
        usage="python verify_evidence.py [--json] [--timeout SECONDS] [--save PATH] <command ...>"
    )
    parser.add_argument("--json", action="store_true", help="Output machine-parseable JSON receipt")
    parser.add_argument("--timeout", type=int, default=300, help="Command timeout in seconds (default: 300)")
    parser.add_argument("--save", type=str, default=None, help="Save JSON verification certificate to file")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="The command line string to verify")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmd = " ".join(args.command)
    if not args.json:
        print(f"[*] Running Gate Verification: '{cmd}'")

    report = run_verification(cmd, timeout=args.timeout)

    if args.save:
        save_path = Path(args.save)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        if not args.json:
            print(f"[*] Verification receipt saved to '{save_path}'")

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("\n--- GATE VERIFICATION RESULT ---")
        if report["passed"]:
            print(f"✅ PASSED (Exit Code: {report['exit_code']}, Duration: {report['duration_seconds']}s)")
            if report["stdout"]:
                print(f"Output:\n{report['stdout']}")
        else:
            print(f"❌ FAILED (Exit Code: {report['exit_code']}, Duration: {report['duration_seconds']}s)")
            if report["stderr"]:
                print(f"Error:\n{report['stderr']}")
            elif report["stdout"]:
                print(f"Output:\n{report['stdout']}")
            if report.get("error_message"):
                print(f"Details: {report['error_message']}")

    sys.exit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
