"""Turn raw iJudge problem records into the registry shape both repos consume.

Category flags come from the title tags configured in data/course.json, and
once a flag has been seen it stays set: iJudge drops tags such as [Recommend]
from a title after its deadline passes.
"""

from __future__ import annotations

from typing import Any, Mapping

from . import config
from .client import BASE_URL
from .weeks import format_expire_date

# Fields written to the summary registry (data/oj_problems.json). The detail
# registry adds course_page, courseProblem, problem, sampleCases, submission,
# beforeCode.
SUMMARY_FIELDS = (
    "id", "name", "week", "status", "difficulty", "passed_count",
    "attempt_count", "percentage", "expire_date", "released", "is_learning_log",
    "is_recommended", "is_midterm", "is_mini_exam", "url",
)

# registry flag -> category name in course.json
FLAG_CATEGORIES = {
    "is_learning_log": "learning_log",
    "is_recommended": "recommended",
    "is_midterm": "midterm",
    "is_mini_exam": "mini_exam",
}


def build_problem_item(
    raw: Mapping[str, Any],
    index: int,
    existing: Mapping[int, Mapping[str, Any]] | None = None,
    details: Mapping[int, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Normalise one raw `cp_*` record from the course listing.

    `index` is the problem's position in the listing, which determines the
    ?problemPage= value in its URL. `existing` (summary records) and `details`
    (detail records) supply sticky flags, the stored week and, when the
    listing omits it, the release time.
    """
    pid = raw["cp_id"]
    name = raw.get("cp_title", "") or ""
    attempted = raw.get("attempted", 0) or 0
    passed = raw.get("passed", 0) or 0
    prev = (existing or {}).get(pid, {})
    prev_detail = (details or {}).get(pid, {})

    flags = {
        flag: config.has_category(name, category) or bool(prev.get(flag))
        for flag, category in FLAG_CATEGORIES.items()
    }
    # Keep the [Recommend] marker in the name once iJudge has dropped it, so
    # the title still shows why the problem is listed as recommended.
    if flags["is_recommended"] and not config.has_category(name, "recommended"):
        name = f"[Recommend] {name}"

    if raw.get("status", "") == "PASSED":
        status = "Passed"
    elif attempted > 0:
        status = "Not Passed"
    else:
        status = "Not Submit"

    released = (
        raw.get("cp_release_time")
        or (prev_detail.get("courseProblem") or {}).get("cp_release_time")
        or prev.get("released")
    )

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
        "released": released,
        **flags,
        "url": f"{BASE_URL}/problems/{pid}/description?problemPage={page_num}",
        "course_page": page_num,
    }
    item["week"] = config.get_week(pid, name, released, fallback=prev.get("week"))
    return item


def summary_fields(item: Mapping[str, Any]) -> dict[str, Any]:
    """Project a full item down to the summary registry's field set."""
    return {k: item[k] for k in SUMMARY_FIELDS if k in item}
