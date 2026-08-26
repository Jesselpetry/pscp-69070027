#!/usr/bin/env python3
"""
Sync OJ Problem folder names, checkmark tags (✅), and verify that all
problems in pscp-69070027 match live iJudge status and repository conventions.
"""

import json
import os
import re

PSCP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OJ_DIR = os.path.join(PSCP_ROOT, "oj")
DETAIL_JSON = os.path.join(PSCP_ROOT, "data", "all_problems_detail.json")

EARLIER_PASSED_PIDS = {
    2981, 2988, 2992, 2995, 2997, 2998, 2999, 3002, 3004, 3005, 3006, 3008, 3010,
    3014, 3015, 3016, 3018, 3019, 3020, 3021, 3023, 3027, 3030, 3032, 3033, 3034,
    3035, 3037, 3038, 3039, 3040, 3041
}

def sync_status():
    if not os.path.exists(DETAIL_JSON):
        print(f"Error: {DETAIL_JSON} not found. Run scrape_all_oj_problems.py first.")
        return

    with open(DETAIL_JSON, "r", encoding="utf-8") as f:
        active_details = json.load(f)
    active_map = {p["id"]: p for p in active_details}

    renames = 0
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
        if target_name != d:
            new_path = os.path.join(OJ_DIR, target_name)
            os.rename(dir_path, new_path)
            print(f"Renamed: {d} -> {target_name}")
            renames += 1

    print(f"Status sync completed. ({renames} folders renamed)")

if __name__ == "__main__":
    sync_status()
