"""Turn raw iJudge problem records into the registry shape both repos consume.

The scraper and the sync script previously built this dict independently, with
subtly different field sets; the summary/detail split is now explicit.
"""

from __future__ import annotations

from typing import Any, Mapping

from .client import BASE_URL
from .weeks import format_expire_date, get_week

MIDTERM_RANGE = (3274, 3282)

# Fields written to the summary registry (oj_problems.json). The detail registry
# adds course_page, courseProblem, problem, sampleCases, submission, beforeCode.
SUMMARY_FIELDS = (
    "id", "name", "week", "status", "difficulty", "passed_count",
    "attempt_count", "percentage", "expire_date", "is_learning_log",
    "is_recommended", "is_midterm", "url",
)


def build_problem_item(
    raw: Mapping[str, Any],
    index: int,
    existing: Mapping[int, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Normalise one raw `cp_*` record from the course listing.

    `index` is the problem's position in the listing, which determines the
    ?problemPage= value in its URL. `existing` preserves the [Recommend] flag,
    which iJudge drops from the title once a deadline passes.
    """
    pid = raw["cp_id"]
    name = raw.get("cp_title", "") or ""
    attempted = raw.get("attempted", 0) or 0
    passed = raw.get("passed", 0) or 0

    upper = name.upper()
    is_learning_log = "[LEARNING LOG" in upper
    is_recommended = "[RECOMMEND" in upper
    is_midterm = "[ MIDTERM ]" in upper or MIDTERM_RANGE[0] <= pid <= MIDTERM_RANGE[1]

    # A problem flagged as recommended in a previous run stays recommended even
    # after iJudge stops advertising it in the title.
    if existing and existing.get(pid, {}).get("is_recommended"):
        is_recommended = True
        if "[recommend]" not in name.lower():
            name = f"[Recommend] {name}"

    if raw.get("status", "") == "PASSED":
        status = "Passed"
    elif attempted > 0:
        status = "Not Passed"
    else:
        status = "Not Submit"

    page_num = index // 10
    item: dict[str, Any] = {
        "id": pid,
        "name": name,
        "status": status,
        "difficulty": raw.get("problem_level", 0),
        "passed_count": passed,
        "attempt_count": attempted,
        "percentage": round(passed / attempted * 100, 2) if attempted > 0 else 0.0,
        "expire_date": format_expire_date(raw.get("cp_expired_time", "")),
        "is_learning_log": is_learning_log,
        "is_recommended": is_recommended,
        "is_midterm": is_midterm,
        "url": f"{BASE_URL}/problems/{pid}/description?problemPage={page_num}",
        "course_page": page_num,
    }
    item["week"] = get_week(item)
    return item


def summary_fields(item: Mapping[str, Any]) -> dict[str, Any]:
    """Project a full item down to the summary registry's field set."""
    return {k: item[k] for k in SUMMARY_FIELDS if k in item}
