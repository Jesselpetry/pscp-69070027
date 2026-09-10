#!/usr/bin/env python3
"""
Sync OJ Problem folder names, checkmark tags (✅), and verify that all
problems in pscp-69070027 match live iJudge status and repository conventions.

Run:  python3 scripts/sync_oj_status.py [--dry-run]

Renaming is destructive and not trivially reversible (the ✅ suffix encodes
state that only exists on iJudge), so `--dry-run` prints the planned renames
to stderr and touches nothing.
"""

import argparse
import json
import os
import re
import sys

PSCP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OJ_DIR = os.path.join(PSCP_ROOT, "oj")
DETAIL_JSON = os.path.join(PSCP_ROOT, "data", "all_problems_detail.json")

EARLIER_PASSED_PIDS = {
    2981, 2988, 2992, 2995, 2997, 2998, 2999, 3002, 3004, 3005, 3006, 3008, 3010,
    3014, 3015, 3016, 3018, 3019, 3020, 3021, 3023, 3027, 3030, 3032, 3033, 3034,
    3035, 3037, 3038, 3039, 3040, 3041
}


def sync_status(dry_run: bool = False) -> int:
    if not os.path.exists(DETAIL_JSON):
        print(
            f"Error: {DETAIL_JSON} not found. Run scrape_all_oj_problems.py first.",
            file=sys.stderr,
        )
        return 1

    with open(DETAIL_JSON, "r", encoding="utf-8") as f:
        active_details = json.load(f)
    active_map = {p["id"]: p for p in active_details}

    renames = 0
    skipped = 0
    for d in sorted(os.listdir(OJ_DIR)):
        dir_path = os.path.join(OJ_DIR, d)
        if not os.path.isdir(dir_path):
            continue

        m = re.match(r"^oj(\d+)-(.*?)(?: ✅)?$", d)
        if not m:
            continue

        pid = int(m.group(1))
        base_name = m.group(2).strip()

        # Clean double underscores
        base_name = re.sub(r"_+", "_", base_name)

        is_passed = False
        if pid in active_map:
            is_passed = (active_map[pid]["status"] == "Passed")
        elif pid in EARLIER_PASSED_PIDS:
            is_passed = True

        target_name = f"oj{pid}-{base_name} ✅" if is_passed else f"oj{pid}-{base_name}"
        if target_name == d:
            continue

        new_path = os.path.join(OJ_DIR, target_name)

        # os.rename onto an existing directory either raises (non-empty) or
        # silently replaces (empty) depending on the platform. Neither is a
        # good outcome for a folder holding a solution, so refuse instead.
        if os.path.exists(new_path):
            print(
                f"[SKIP] target already exists, not renaming: "
                f"{d!r} -> {target_name!r}",
                file=sys.stderr,
            )
            skipped += 1
            continue

        if dry_run:
            print(f"[DRY-RUN] Would rename: {d!r} -> {target_name!r}", file=sys.stderr)
        else:
            os.rename(dir_path, new_path)
            print(f"Renamed: {d} -> {target_name}")
        renames += 1

    if dry_run:
        print(
            f"[DRY-RUN] Status sync preview complete. "
            f"({renames} folders would be renamed, {skipped} skipped)",
            file=sys.stderr,
        )
    else:
        print(f"Status sync completed. ({renames} folders renamed, {skipped} skipped)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync oj/ folder names with iJudge pass status."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview directory renames and file modifications without executing changes.",
    )
    args = parser.parse_args()
    return sync_status(dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
