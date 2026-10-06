#!/usr/bin/env python3
"""Regenerate the problem folders on main from the OP registries, offline.

For every problem in data/oj_problems.json (or the --only selection):

  * create the folder if it is missing (Learning Logs at the root as
    oj<id>/, everything else under oj/), and add or drop the ✅ suffix of an
    oj/ folder to match the registry status
  * write problem.md from data/all_problems_detail.json when it is missing
    or is a generated file whose content differs; a hand-written problem.md
    (no generated marker, no legacy heading) is never touched, nor is any
    problem.md of a problem without a detail record (2981)
  * create main.py from the stub template if missing, and refresh it only
    while it is still an untouched stub (cleans [TAG]s out of docstrings)

recommended/ is never written. No network access: run the scraper first to
refresh the registries. Running it twice in a row changes nothing the second
time.

Run (from the repo root):
    python3 .op/scripts/render_problems.py [--dry-run] [--check] [--only IDS]

Exit codes: 0 ok, 1 --check found changes, 2 bad arguments or registry.
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ijudge import fsio, paths, render  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Regenerate problem.md, main.py stubs and ✅ folder names "
                    "on main from the OP registries (offline).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned changes to stderr and write nothing.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Write nothing; exit 1 if anything would change (for CI/hooks).",
    )
    parser.add_argument(
        "--only",
        metavar="IDS",
        help="Limit to these ids/ranges, e.g. 3226,3290-3301.",
    )
    args = parser.parse_args()

    try:
        only = render.parse_ids(args.only) if args.only else None
    except ValueError:
        parser.error(f"--only could not be parsed: {args.only!r}")

    fsio.set_dry_run(args.dry_run or args.check)
    if not os.path.isdir(paths.MAIN_ROOT):
        print(f"[!] main checkout not found: {paths.MAIN_ROOT}", file=sys.stderr)
        return 2
    try:
        summaries = render.load_registry(paths.SUMMARY_JSON)
        details = render.load_registry(paths.DETAIL_JSON)
    except (OSError, ValueError, KeyError) as e:
        print(f"[!] could not read the registries: {e}", file=sys.stderr)
        return 2
    if not summaries:
        print(f"[!] {paths.SUMMARY_JSON} is missing or empty; run the scraper first.",
              file=sys.stderr)
        return 2

    if only is not None:
        unknown = sorted(only - set(summaries))
        if unknown:
            print(f"[WARN] {len(unknown)} selected id(s) not in the summary "
                  f"registry, skipped: {', '.join(map(str, unknown[:20]))}",
                  file=sys.stderr)
        only &= set(summaries)

    print(f"Rendering into {paths.MAIN_ROOT}"
          + (" (no writes)" if fsio.is_dry_run() else ""))
    stats = render.render_ids(only, summaries=summaries, details=details)
    print(stats.report())

    if fsio.is_dry_run():
        print(f"{stats.changes} change(s) would be made.")
    else:
        print(f"{stats.changes} change(s) made.")
    if args.check and stats.changes:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
