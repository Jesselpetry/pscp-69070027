#!/usr/bin/env python3
"""Add or remove the ` ✅` suffix on oj/ folders to match the registry status.

The status comes from the summary registry (data/oj_problems.json), which the
scraper refreshes from iJudge -- `scrape_all_oj_problems.py --fast` is enough.
Learning Log folders at the repo root never carry the suffix and are left
alone; render_problems.py applies the same rule while rendering.

Run (from the repo root):
    python3 .op/scripts/sync_oj_status.py [--dry-run]

Renaming moves the student's folder, so `--dry-run` prints the planned renames
to stderr and touches nothing. A rename onto an existing folder is refused.

Exit codes: 0 ok, 1 a rename was refused, 2 the registry could not be read.
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ijudge import fsio, paths, render  # noqa: E402


def sync_status() -> int:
    try:
        registry = render.load_registry(paths.SUMMARY_JSON)
    except (OSError, ValueError, KeyError) as e:
        print(f"Error: could not read {paths.SUMMARY_JSON}: {e}", file=sys.stderr)
        return 2
    if not registry:
        print(
            f"Error: {paths.SUMMARY_JSON} is missing or empty. "
            f"Run scrape_all_oj_problems.py --fast first.",
            file=sys.stderr,
        )
        return 2
    if not os.path.isdir(paths.OJ_DIR):
        print(f"Error: {paths.OJ_DIR} not found.", file=sys.stderr)
        return 2

    renames = refused = 0
    unknown: list[str] = []
    for name in sorted(os.listdir(paths.OJ_DIR)):
        folder = os.path.join(paths.OJ_DIR, name)
        pid = paths.problem_id_of(name)
        if pid is None or not os.path.isdir(folder):
            continue
        item = registry.get(pid)
        if item is None:
            unknown.append(name)
            continue

        desired = render.status_folder(item, folder)
        if desired == folder:
            continue
        if os.path.exists(desired):
            render.sync_folder_status(item, folder)  # prints the refusal
            refused += 1
            continue
        render.sync_folder_status(item, folder)
        if not fsio.is_dry_run():
            print(f"Renamed: {name} -> {os.path.basename(desired)}")
        renames += 1

    if unknown:
        print(f"[WARN] not in the registry, left as is: {', '.join(unknown)}",
              file=sys.stderr)
    verb = "would be renamed" if fsio.is_dry_run() else "renamed"
    print(f"Status sync complete: {renames} folder(s) {verb}, {refused} refused, "
          f"{len(registry)} problems in the registry.")
    return 1 if refused else 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync the ✅ suffix of oj/ folders with the registry pass status."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned renames to stderr and touch nothing.",
    )
    args = parser.parse_args()
    fsio.set_dry_run(args.dry_run)
    return sync_status()


if __name__ == "__main__":
    sys.exit(main())
