#!/usr/bin/env python3
"""Run a problem's main.py against the official samples in the detail registry.

    python3 .op/scripts/run_samples.py 3290-3292 2988
    python3 .op/scripts/run_samples.py --week 9
    python3 .op/scripts/run_samples.py --solutions 3355   # test the archived copy

Outputs are compared the way a judge forgives whitespace: CRLF -> LF, trailing
spaces on each line and trailing blank lines are ignored, nothing else is.
Untouched stubs are skipped, not failed, so a whole week can be checked while
it is still half done.

Exit codes: 0 no failures, 1 at least one sample failed, 2 bad arguments.
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import subprocess
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ijudge import code, config, paths  # noqa: E402

TIMEOUT_S = 10
DIFF_LINES = 12


def parse_ids(tokens: list[str]) -> set[int]:
    """'3290-3292' '2988' '3290,3291' -> ids."""
    ids: set[int] = set()
    for token in tokens:
        for part in token.replace(",", " ").split():
            lo, sep, hi = part.partition("-")
            if sep and lo.isdigit() and hi.isdigit():
                a, b = sorted((int(lo), int(hi)))
                ids.update(range(a, b + 1))
            elif not sep and part.isdigit():
                ids.add(int(part))
            else:
                raise ValueError(f"bad problem id: {part!r}")
    return ids


def normalise(text: str) -> list[str]:
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    return lines


def load_json(path: str) -> list[dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_once(main_py: str, stdin: str) -> tuple[str, str]:
    """Run main.py once; return (verdict detail, stdout). Detail '' = ran fine."""
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    try:
        proc = subprocess.run(
            [sys.executable, os.path.basename(main_py)],
            input=stdin,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=TIMEOUT_S,
            cwd=os.path.dirname(main_py),
            env=env,
        )
    except subprocess.TimeoutExpired:
        return f"timed out after {TIMEOUT_S}s", ""
    if proc.returncode != 0:
        last = (proc.stderr.strip().splitlines() or [""])[-1]
        return f"exit code {proc.returncode}: {last}".rstrip(": "), proc.stdout
    return "", proc.stdout


def short_diff(expected: list[str], actual: list[str]) -> list[str]:
    diff = list(difflib.unified_diff(
        expected, actual, "expected", "actual", lineterm="", n=1
    ))
    if len(diff) > DIFF_LINES:
        diff = diff[:DIFF_LINES] + [f"... ({len(diff) - DIFF_LINES} more diff lines)"]
    return diff


def test_problem(pid: int, record: dict[str, Any] | None, use_archive: bool) -> dict[str, int]:
    counts = {"pass": 0, "fail": 0, "skip": 0}
    title = config.clean_title((record or {}).get("name"))
    head = f"oj{pid} {title}".rstrip()

    if use_archive:
        main_py: str | None = paths.solution_file(pid)
    else:
        folder = paths.find_problem_dir(pid)
        main_py = os.path.join(folder, "main.py") if folder else None
    if not main_py or not os.path.isfile(main_py):
        print(f"{head}: missing (no main.py{' in the archive' if use_archive else ''})")
        counts["skip"] += 1
        return counts
    with open(main_py, "r", encoding="utf-8") as f:
        if code.is_stub(f.read()):
            print(f"{head}: stub")
            counts["skip"] += 1
            return counts

    samples = (record or {}).get("sampleCases") or []
    if not samples:
        print(f"{head}: no samples in the registry")
        counts["skip"] += 1
        return counts

    base = paths.OP_ROOT if use_archive else paths.MAIN_ROOT
    print(f"{head}  ({os.path.relpath(main_py, base)})")
    for i, case in enumerate(samples, 1):
        # iJudge stores some samples with CRLF; programs split lines on LF.
        stdin = (case.get("testcase_input") or "").replace("\r\n", "\n")
        expected = normalise(case.get("testcase_output") or "")
        problem, stdout = run_once(main_py, stdin)
        actual = normalise(stdout)
        if not problem and actual == expected:
            print(f"  sample {i}: PASS")
            counts["pass"] += 1
            continue
        counts["fail"] += 1
        print(f"  sample {i}: FAIL{' (' + problem + ')' if problem else ''}")
        # A crash or timeout with no output says it all; skip the diff.
        if actual != expected and (actual or not problem):
            for line in short_diff(expected, actual):
                print(f"    {line}")
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run main.py against the official sample cases."
    )
    parser.add_argument("ids", nargs="*", help="problem ids or ranges, e.g. 3290-3292 2988")
    parser.add_argument("--week", type=int, action="append", metavar="N",
                        help="every problem of week N (repeatable)")
    parser.add_argument("--solutions", action="store_true",
                        help="test the archived solutions/oj<id>/main.py instead of main")
    args = parser.parse_args()

    try:
        ids = parse_ids(args.ids)
    except ValueError as e:
        parser.error(str(e))
    if args.week:
        summary = load_json(paths.SUMMARY_JSON)
        ids.update(p["id"] for p in summary if p.get("week") in set(args.week))
    if not ids:
        parser.error("give problem ids/ranges or --week N")

    details = {p["id"]: p for p in load_json(paths.DETAIL_JSON)}
    totals = {"pass": 0, "fail": 0, "skip": 0}
    failed: list[int] = []
    for pid in sorted(ids):
        counts = test_problem(pid, details.get(pid), args.solutions)
        for k, v in counts.items():
            totals[k] += v
        if counts["fail"]:
            failed.append(pid)

    print(
        f"\nTotal: {totals['pass']} passed, {totals['fail']} failed samples, "
        f"{totals['skip']} problems skipped"
        + (f" | failing: {', '.join(map(str, failed))}" if failed else "")
    )
    return 1 if totals["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
