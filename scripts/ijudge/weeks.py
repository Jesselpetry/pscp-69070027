"""Course-week classification and iJudge date formatting.

Week numbers come from data/course.json (see ijudge.config): per-problem
overrides, then category weeks, then the release-date window. There are no
problem-id ranges in code any more.
"""

from __future__ import annotations

import re
from typing import Any, Mapping

from . import config

MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

_ISO_PREFIX = re.compile(r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})")


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


def release_of(item: Mapping[str, Any]) -> str | None:
    """Release timestamp of a registry record, summary or detail shape."""
    course_problem = item.get("courseProblem") or {}
    return (
        item.get("released")
        or course_problem.get("cp_release_time")
        or item.get("cp_release_time")
    )


def get_week(item: Mapping[str, Any]) -> int | None:
    """Teaching week of a registry record.

    Falls back to the week already stored on the record, so a problem whose
    release date is unknown keeps its number instead of being reset.
    """
    return config.get_week(
        item["id"], item.get("name"), release_of(item), fallback=item.get("week")
    )
