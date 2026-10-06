#!/usr/bin/env python3
"""Keep the solution archive (OP: solutions/oj<id>/main.py) in step with main.

    python3 .op/scripts/archive_solutions.py                  # archive new work
    python3 .op/scripts/archive_solutions.py --update         # also overwrite changed copies
    python3 .op/scripts/archive_solutions.py --restore 3355   # archive -> main (stubs only)
    python3 .op/scripts/archive_solutions.py --blank 3290-3292 # main -> fresh stub

The student's main.py is the source of truth and the archive is the safety
net, so every mode refuses anything that could lose code: stubs are never
archived, a changed archive copy is only overwritten with --update, --restore
only fills a stub, and --blank only clears code the archive holds verbatim.

Exit codes: 0 everything in step / done, 1 something needs attention (changed
copies not updated, an id refused or missing), 2 bad arguments.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Iterable

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ijudge import code, config, fsio, paths  # noqa: E402


def parse_ids(tokens: Iterable[str]) -> list[int]:
    """'3290-3292,2988' / ['3290', '3291'] -> sorted unique ids."""
    ids: set[int] = set()
    for token in tokens:
        for part in token.replace(",", " ").split():
            if "-" in part:
                lo, hi = part.split("-", 1)
                if not (lo.isdigit() and hi.isdigit()):
                    raise ValueError(f"bad id range: {part!r}")
                a, b = sorted((int(lo), int(hi)))
                ids.update(range(a, b + 1))
            elif part.isdigit():
                ids.add(int(part))
            else:
                raise ValueError(f"bad problem id: {part!r}")
    return sorted(ids)


def read_text(path: str) -> str | None:
    """File contents with line endings untouched, or None if absent."""
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def load_names() -> dict[int, str]:
    """Problem id -> iJudge title, from the summary registry."""
    try:
        with open(paths.SUMMARY_JSON, "r", encoding="utf-8") as f:
            return {p["id"]: p.get("name", "") for p in json.load(f)}
    except (OSError, ValueError) as e:
        print(f"[!] Warning: cannot read {paths.SUMMARY_JSON}: {e}", file=sys.stderr)
        return {}


class Archive:
    def __init__(self, solutions_dir: str):
        self.root = solutions_dir
        self.folders = paths.index_problem_dirs()

    def archive_file(self, pid: int) -> str:
        return os.path.join(self.root, f"oj{pid}", "main.py")

    def main_file(self, pid: int) -> str | None:
        folder = self.folders.get(pid)
        return os.path.join(folder, "main.py") if folder else None

    def archived_ids(self) -> list[int]:
        if not os.path.isdir(self.root):
            return []
        found = []
        for d in os.listdir(self.root):
            if d.startswith("oj") and d[2:].isdigit() and os.path.isfile(
                os.path.join(self.root, d, "main.py")
            ):
                found.append(int(d[2:]))
        return sorted(found)


def report(pid: int, status: str, detail: str = "") -> None:
    line = f"  oj{pid:<5} {status:<14}"
    print(f"{line} {detail}".rstrip())


def sync(arc: Archive, ids: list[int] | None, update: bool) -> int:
    """Copy solved main.py files into the archive."""
    explicit = ids is not None
    targets = ids if explicit else sorted(arc.folders)
    totals = dict.fromkeys(
        ["archived", "updated", "changed", "up to date", "stub", "missing"], 0
    )
    for pid in targets:
        main_py = arc.main_file(pid)
        src = read_text(main_py) if main_py else None
        if src is None:
            totals["missing"] += 1
            report(pid, "missing", "no main.py on main")
            continue
        if code.is_stub(src):
            totals["stub"] += 1
            if explicit:
                report(pid, "stub", "not archived")
            continue
        dst = arc.archive_file(pid)
        old = read_text(dst)
        if old == src:
            totals["up to date"] += 1
            if explicit:
                report(pid, "up to date")
        elif old is None:
            fsio.write_text(dst, src)
            totals["archived"] += 1
            report(pid, "archived", os.path.relpath(dst, os.path.dirname(arc.root)))
        elif update:
            fsio.write_text(dst, src)
            totals["updated"] += 1
            report(pid, "updated", "archive overwritten with main")
        else:
            totals["changed"] += 1
            report(pid, "changed", "main differs from archive (--update to overwrite)")

    # Code that exists only in the archive is worth pointing out: it is what
    # --restore is for, and it is otherwise invisible from main.
    only_archived = []
    for pid in arc.archived_ids():
        if explicit and pid not in targets:
            continue
        main_py = arc.main_file(pid)
        src = read_text(main_py) if main_py else None
        if src is None or code.is_stub(src):
            only_archived.append(pid)
    if only_archived:
        print(
            "  archive only:  "
            + ", ".join(str(p) for p in only_archived)
            + "  (main has a stub; --restore to bring the code back)"
        )

    print(
        "Total: " + ", ".join(f"{n} {k}" for k, n in totals.items())
        + f", {len(only_archived)} archive only"
    )
    attention = totals["changed"] + (totals["missing"] if explicit else 0)
    return 1 if attention else 0


def restore(arc: Archive, ids: list[int]) -> int:
    """Copy archived code back to main, only over an untouched stub."""
    done = refused = 0
    for pid in ids:
        saved = read_text(arc.archive_file(pid))
        main_py = arc.main_file(pid)
        if saved is None:
            refused += 1
            report(pid, "not archived", "nothing to restore")
            continue
        if main_py is None:
            refused += 1
            report(pid, "no folder", "problem folder missing on main (run render first)")
            continue
        current = read_text(main_py)
        if current == saved:
            report(pid, "up to date", "main already has the archived code")
            continue
        if current is not None and not code.is_stub(current):
            refused += 1
            report(pid, "refused", "main has its own code; not overwriting")
            continue
        fsio.write_text(main_py, saved)
        done += 1
        report(pid, "restored", os.path.relpath(main_py, paths.MAIN_ROOT))
    print(f"Total: {done} restored, {refused} refused/missing")
    return 1 if refused else 0


def blank(arc: Archive, ids: list[int]) -> int:
    """Reset main.py to the stub, only when the archive holds the same code."""
    names = load_names()
    done = refused = 0
    for pid in ids:
        main_py = arc.main_file(pid)
        current = read_text(main_py) if main_py else None
        if current is None:
            refused += 1
            report(pid, "missing", "no main.py on main")
            continue
        if code.is_stub(current):
            report(pid, "already stub")
            continue
        saved = read_text(arc.archive_file(pid))
        if saved is None:
            refused += 1
            report(pid, "refused", "not archived yet (run without --blank first)")
            continue
        if saved != current:
            refused += 1
            report(pid, "refused", "archive differs from main (sync with --update first)")
            continue
        if pid not in names:
            refused += 1
            report(pid, "refused", "no title in the registry for the stub")
            continue
        fsio.write_text(main_py, code.stub_solution(config.clean_title(names[pid])))
        done += 1
        report(pid, "blanked", os.path.relpath(main_py, paths.MAIN_ROOT))
    print(f"Total: {done} blanked, {refused} refused/missing")
    return 1 if refused else 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync solutions/oj<id>/main.py (OP) with the student's main.py on main."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--restore", nargs="+", metavar="IDS",
                      help="copy archived code back to main where main.py is a stub")
    mode.add_argument("--blank", nargs="+", metavar="IDS",
                      help="reset main.py to the stub where the archive holds identical code")
    parser.add_argument("--ids", nargs="+", metavar="IDS",
                        help="limit the default sync to these ids/ranges (e.g. 3290-3292 2988)")
    parser.add_argument("--update", action="store_true",
                        help="overwrite archive copies that differ from main")
    parser.add_argument("--solutions-dir", default=paths.SOLUTIONS_DIR, metavar="PATH",
                        help="archive location (default: %(default)s)")
    parser.add_argument("--dry-run", action="store_true",
                        help="print planned writes to stderr, touch nothing")
    args = parser.parse_args()

    if (args.restore or args.blank) and (args.ids or args.update):
        parser.error("--ids/--update apply to the default sync only")
    try:
        ids = parse_ids(args.ids) if args.ids else None
        restore_ids = parse_ids(args.restore) if args.restore else None
        blank_ids = parse_ids(args.blank) if args.blank else None
    except ValueError as e:
        parser.error(str(e))

    # Keep stdout in step with fsio's [DRY-RUN] lines on stderr.
    sys.stdout.reconfigure(line_buffering=True)
    fsio.set_dry_run(args.dry_run)
    arc = Archive(os.path.abspath(os.path.expanduser(args.solutions_dir)))
    print(f"main:    {paths.MAIN_ROOT}")
    print(f"archive: {arc.root}")
    if args.dry_run:
        print("dry run: statuses below are planned, nothing is written")
    if restore_ids is not None:
        return restore(arc, restore_ids)
    if blank_ids is not None:
        return blank(arc, blank_ids)
    return sync(arc, ids, args.update)


if __name__ == "__main__":
    sys.exit(main())
