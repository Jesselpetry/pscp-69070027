#!/usr/bin/env python3
"""Read-only consistency check of the registry, course.json, main and solutions/.

Run from the repo root:  python3 .op/scripts/check_repo.py [--quiet]

Errors are states the other scripts cannot work with (a registry record with
no folder, two folders for one id, a stored week that disagrees with
course.json); they make the exit status 1. Warnings are drift that a routine
command fixes (sync, archive, a new course.json week) or work still to do (a
Learning Log without submission.md); they are reported but do not fail.

Nothing is written, so it is safe to run at any time.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ijudge import code, config, paths, weeks  # noqa: E402
from ijudge.course import FLAG_CATEGORIES  # noqa: E402

PASS_SUFFIX = " ✅"
MAX_LISTED = 40


class Report:
    """Findings grouped by check, in the order the checks run."""

    def __init__(self) -> None:
        self.groups: dict[tuple[str, str], list[str]] = {}

    def add(self, level: str, check: str, item: str) -> None:
        self.groups.setdefault((level, check), []).append(item)

    def count(self, level: str) -> int:
        return sum(len(v) for (lvl, _), v in self.groups.items() if lvl == level)

    def print(self, quiet: bool) -> None:
        for level, title in (("error", "Errors"), ("warning", "Warnings")):
            groups = [(c, items) for (lvl, c), items in self.groups.items() if lvl == level]
            if not groups:
                if not quiet:
                    print(f"== {title}: none ==")
                continue
            print(f"== {title} ({self.count(level)}) ==")
            for check, items in groups:
                print(f"- {check} ({len(items)})")
                for item in items[:MAX_LISTED]:
                    print(f"    {item}")
                if len(items) > MAX_LISTED:
                    print(f"    ... and {len(items) - MAX_LISTED} more")


def ids_text(ids: list[int]) -> str:
    return ", ".join(str(i) for i in sorted(ids))


def read_text(path: str) -> str | None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeDecodeError):
        return None


def scan_folders() -> dict[int, list[str]]:
    """Every problem folder on main per id, unlike index_problem_dirs()
    which keeps one and so hides duplicates."""
    found: dict[int, list[str]] = defaultdict(list)
    if os.path.isdir(paths.OJ_DIR):
        for d in sorted(os.listdir(paths.OJ_DIR)):
            pid = paths.problem_id_of(d)
            if pid is not None and os.path.isdir(os.path.join(paths.OJ_DIR, d)):
                found[pid].append(os.path.join(paths.OJ_DIR, d))
    if os.path.isdir(paths.MAIN_ROOT):
        for d in sorted(os.listdir(paths.MAIN_ROOT)):
            full = os.path.join(paths.MAIN_ROOT, d)
            if re.fullmatch(r"oj\d+", d) and os.path.isdir(full):
                found[int(d[2:])].append(full)
    return found


def scan_solutions() -> set[int]:
    if not os.path.isdir(paths.SOLUTIONS_DIR):
        return set()
    return {
        int(d[2:]) for d in os.listdir(paths.SOLUTIONS_DIR)
        if re.fullmatch(r"oj\d+", d) and os.path.isdir(os.path.join(paths.SOLUTIONS_DIR, d))
    }


def rel(path: str) -> str:
    return os.path.relpath(path, paths.MAIN_ROOT)


# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------

def check_course(report: Report) -> None:
    entries = config.load_course().get("weeks", [])
    dupes = [w for w, n in Counter(int(e["week"]) for e in entries).items() if n > 1]
    for w in sorted(dupes):
        report.add("error", "course.json: duplicate week number", f"week {w}")
    prev: tuple[int, date] | None = None
    for e in entries:
        if not e.get("from"):
            continue
        try:
            start = date.fromisoformat(e["from"])
        except ValueError:
            report.add("error", "course.json: bad `from` date", f"week {e['week']}: {e['from']!r}")
            continue
        if prev and start <= prev[1]:
            report.add(
                "error", "course.json: `from` dates not strictly increasing",
                f"week {e['week']} ({start}) is not after week {prev[0]} ({prev[1]})",
            )
        prev = (int(e["week"]), start)


def check_registry(
    report: Report,
    registry: list[dict[str, Any]],
    folders: dict[int, list[str]],
    solutions: set[int],
) -> None:
    by_id = {r["id"]: r for r in registry}

    missing = [pid for pid in by_id if pid not in folders]
    if missing:
        report.add("error", "registry record with no folder on main", ids_text(missing))
    orphans = [pid for pid in folders if pid not in by_id]
    for pid in sorted(orphans):
        report.add("error", "folder on main with no registry record",
                   ", ".join(rel(f) for f in folders[pid]))
    for pid, dirs in sorted(folders.items()):
        if len(dirs) > 1:
            report.add("error", "more than one folder for one id",
                       f"{pid}: " + " | ".join(rel(d) for d in dirs))

    for r in registry:
        stored = r.get("week")
        if stored is None:
            report.add("error", "registry record without a week", str(r["id"]))
            continue
        expected = weeks.get_week(r)
        if expected != stored:
            report.add("error", "stored week differs from course.json",
                       f"{r['id']}: stored {stored}, course.json says {expected}")

    outside = []
    for r in registry:
        released = config.release_date(weeks.release_of(r))
        if released is not None and config.week_for_release(released) is None:
            outside.append(f"{r['id']} (released {released})")
    if outside:
        report.add("warning", "release date outside every course.json week (add a week)",
                   ", ".join(outside))

    for r in registry:
        dirs = folders.get(r["id"], [])
        for d in dirs:
            if os.path.dirname(d) != paths.OJ_DIR:
                continue
            has_mark = d.endswith(PASS_SUFFIX)
            passed = r.get("status") == "Passed"
            if has_mark != passed:
                report.add(
                    "warning", "✅ suffix disagrees with registry status (run sync)",
                    f"{rel(d)}: status {r.get('status')!r}",
                )
        if r.get("is_learning_log"):
            for d in dirs:
                if os.path.dirname(d) == paths.MAIN_ROOT and not os.path.isfile(
                    os.path.join(d, "submission.md")
                ):
                    report.add("warning", "Learning Log without submission.md", rel(d))

    for pid, dirs in sorted(folders.items()):
        for d in dirs:
            if not os.path.isfile(os.path.join(d, "problem.md")):
                report.add("warning", "folder without problem.md (run render)", rel(d))

    stray = sorted(solutions - set(by_id))
    if stray:
        report.add("warning", "solutions/ entry with no registry record", ids_text(stray))


def check_solutions(
    report: Report, folders: dict[int, list[str]], solutions: set[int]
) -> tuple[int, int, int]:
    """Compare solved main.py on main with solutions/; return (stubs, solved, no main.py)."""
    stubs = solved = absent = 0
    unarchived, differing = [], []
    for pid, dirs in sorted(folders.items()):
        src = read_text(os.path.join(dirs[0], "main.py"))
        if src is None:
            absent += 1
            continue
        if code.is_stub(src):
            stubs += 1
            continue
        solved += 1
        if pid not in solutions:
            unarchived.append(pid)
            continue
        archived = read_text(paths.solution_file(pid))
        if archived is None:
            unarchived.append(pid)
        elif archived.rstrip() != src.rstrip():
            differing.append(pid)
    if unarchived:
        report.add("warning", "solved on main but not in solutions/ (run archive)",
                   ids_text(unarchived))
    if differing:
        report.add("warning", "solved on main but differs from solutions/ (run archive)",
                   ids_text(differing))
    return stubs, solved, absent


def summary_lines(
    registry: list[dict[str, Any]], counts: tuple[int, int, int], solutions: set[int]
) -> list[str]:
    stubs, solved, absent = counts
    per_cat = {
        cat: sum(1 for r in registry if r.get(flag)) for flag, cat in FLAG_CATEGORIES.items()
    }
    plain = sum(1 for r in registry if not any(r.get(f) for f in FLAG_CATEGORIES))
    passed = sum(1 for r in registry if r.get("status") == "Passed")
    cats = ", ".join(f"{cat} {n}" for cat, n in per_cat.items())
    return [
        "== Summary ==",
        f"registry: {len(registry)} problems, {passed} passed · {cats}, uncategorised {plain}",
        f"main.py on main: {solved} solved, {stubs} stubs"
        + (f", {absent} missing" if absent else "")
        + f" · solutions/: {len(solutions)}",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check registry, course.json, main and solutions/ for consistency (read-only)."
    )
    parser.add_argument("--quiet", action="store_true", help="Print only findings.")
    args = parser.parse_args()

    try:
        with open(paths.SUMMARY_JSON, "r", encoding="utf-8") as f:
            registry = json.load(f)
        config.load_course()
    except (OSError, ValueError) as exc:
        print(f"Error: cannot read the registry or course.json: {exc}", file=sys.stderr)
        return 2

    report = Report()
    folders = scan_folders()
    solutions = scan_solutions()
    check_course(report)
    check_registry(report, registry, folders, solutions)
    counts = check_solutions(report, folders, solutions)

    report.print(args.quiet)
    if not args.quiet:
        for line in summary_lines(registry, counts, solutions):
            print(line)
    return 1 if report.count("error") else 0


if __name__ == "__main__":
    sys.exit(main())
