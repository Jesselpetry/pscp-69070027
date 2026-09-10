"""Course-week classification and iJudge date formatting.

This was duplicated verbatim in four scripts; a new teaching week previously
meant editing all four consistently or the repos silently disagreed.
"""

from __future__ import annotations

import re
from typing import Any, Mapping

MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

_ISO_PREFIX = re.compile(r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})")

_WEEK_5_EXTRA_IDS = {3129, 3135}
_MIDTERM_RANGE = (3274, 3282)
_WEEK_3_4_RANGE = (3058, 3116)
_WEEK_3_MAX_ID = 3072


def format_expire_date(iso_str: str | None) -> str:
    """Render an iJudge ISO timestamp as e.g. '4 September 2026, 23:59'."""
    if not iso_str:
        return ""
    m = _ISO_PREFIX.match(iso_str)
    if not m:
        return iso_str
    year, month_num, day, hour, minute = m.groups()
    month_name = MONTH_NAMES[int(month_num) - 1]
    return f"{int(day)} {month_name} {year}, {hour}:{minute}"


def get_week(item: Mapping[str, Any]) -> int:
    """Classify a problem into its teaching week (1-9).

    Rule order is significant and mirrors the original implementation exactly:
    the week 9 and week 8 deadlines are tested BEFORE the midterm rule, so a
    midterm-flagged problem carrying a late deadline classifies by that deadline
    rather than as week 7. No real problem currently hits that overlap, but the
    committed registries were built with this precedence.

    Falls back to week 1 for anything unrecognised.
    """
    pid = item["id"]
    name = (item.get("name") or "").upper()
    expire = item.get("expire_date") or ""

    if "9 October" in expire or 3349 <= pid <= 3363:
        return 9
    if "25 September" in expire or 3290 <= pid <= 3301:
        return 8
    if item.get("is_midterm") or "[ MIDTERM ]" in name or (
        _MIDTERM_RANGE[0] <= pid <= _MIDTERM_RANGE[1]
    ):
        return 7
    if "11 September" in expire or 3226 <= pid <= 3238:
        return 6
    if "4 September" in expire or pid in _WEEK_5_EXTRA_IDS or 3155 <= pid <= 3167:
        return 5
    # Weeks 3 and 4 share the "28 August" deadline, split by problem id.
    if "28 August" in expire or _WEEK_3_4_RANGE[0] <= pid <= _WEEK_3_4_RANGE[1]:
        return 3 if pid <= _WEEK_3_MAX_ID else 4
    if any(d in expire for d in ("14 August", "16 August", "17 August")) or (
        3020 <= pid <= 3042
    ):
        return 2
    if "31 July" in expire or "7 August" in expire or pid <= 3019:
        return 1
    return 1
