"""Course configuration from data/course.json.

Everything the scripts used to hardcode lives in that file: the week each
release date belongs to, week titles, the title tags that mark a category,
hand-picked folder names for Thai titles, and the midterm course-84 map.
Adding a teaching week means adding one entry to `weeks`, nothing else.
"""

from __future__ import annotations

import json
import re
from datetime import date, datetime, timedelta, timezone
from functools import lru_cache
from typing import Any, Mapping

from .paths import COURSE_CONFIG

_TAG_RE = re.compile(r"\[\s*([^\]]*?)\s*\]")


@lru_cache(maxsize=None)
def load_course(path: str = COURSE_CONFIG) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def course_id(kind: str = "regular") -> int:
    """iJudge course id: "regular" (labs) or "midterm"."""
    return int(load_course()["course_ids"][kind])


# ---------------------------------------------------------------------------
# titles and categories
# ---------------------------------------------------------------------------

def split_title(name: str | None) -> tuple[str, list[str]]:
    """Separate iJudge's bracket tags from the title.

    '[Recommend] [LEARNING LOGS] Temperature' -> ('Temperature',
    ['RECOMMEND', 'LEARNING LOGS']). Whitespace runs collapse to one space.
    """
    raw = name or ""
    tags = [t.upper() for t in _TAG_RE.findall(raw)]
    clean = re.sub(r"\s+", " ", _TAG_RE.sub(" ", raw)).strip()
    return clean or raw.strip(), tags


def clean_title(name: str | None) -> str:
    return split_title(name)[0]


def has_category(name: str | None, category: str) -> bool:
    """True if the title carries a tag configured for `category`."""
    prefixes = load_course()["categories"][category]["tags"]
    _, tags = split_title(name)
    return any(tag.startswith(prefix) for tag in tags for prefix in prefixes)


# ---------------------------------------------------------------------------
# weeks
# ---------------------------------------------------------------------------

def release_date(iso: str | None) -> date | None:
    """iJudge UTC timestamp -> calendar date in the course's timezone."""
    if not iso:
        return None
    try:
        stamp = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return None
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    offset = timezone(timedelta(hours=load_course().get("utc_offset_hours", 0)))
    return stamp.astimezone(offset).date()


def _dated_weeks() -> list[tuple[date, int]]:
    rows = [
        (date.fromisoformat(w["from"]), int(w["week"]))
        for w in load_course()["weeks"]
        if w.get("from")
    ]
    return sorted(rows)


def week_for_release(released: date | None) -> int | None:
    """Week whose window contains `released`.

    A window runs from its `from` date up to the next week's `from`; the last
    one is 7 days long, so a release after it maps to None and the caller
    knows to add a new week to course.json instead of guessing.
    """
    if released is None:
        return None
    rows = _dated_weeks()
    for i, (start, week) in enumerate(rows):
        end = rows[i + 1][0] if i + 1 < len(rows) else start + timedelta(days=7)
        if start <= released < end:
            return week
    return None


def get_week(
    pid: int,
    name: str | None = None,
    released_iso: str | None = None,
    fallback: int | None = None,
) -> int | None:
    """Teaching week of a problem.

    Order: per-problem override, category week (Mini Exam), release-date
    window, then `fallback` (normally the week already in the registry).
    """
    course = load_course()
    override = course.get("week_overrides", {}).get(str(pid))
    if override is not None:
        return int(override)
    for category, spec in course["categories"].items():
        if "week" in spec and has_category(name, category):
            return int(spec["week"])
    week = week_for_release(release_date(released_iso))
    return week if week is not None else fallback


def week_entry(week: int | None) -> Mapping[str, Any]:
    for w in load_course()["weeks"]:
        if w["week"] == week:
            return w
    return {}


def week_label(week: int | None) -> str:
    """'Week 7 / Midterm' style heading label."""
    return week_entry(week).get("label") or f"Week {week}"


def week_title(week: int | None) -> str:
    """Topic of a week, e.g. 'การเรียกซ้ำ (Recursion & Divide and Conquer)'."""
    return week_entry(week).get("title", "")


def known_weeks() -> list[int]:
    return sorted(int(w["week"]) for w in load_course()["weeks"])


# ---------------------------------------------------------------------------
# folders and course mapping
# ---------------------------------------------------------------------------

def folder_name(pid: int, name: str | None) -> str:
    """Folder name for a new problem under oj/ (without the ✅ suffix).

    Uses the hand-picked name from course.json when there is one, else an
    ASCII slug of the title with tag words kept ("[MINI EXAM] Longer" ->
    "MINI_EXAM_Longer", as the existing folders are named). A title with no
    ASCII letters (Thai) falls back to bare `oj<id>`, so it is obvious a name
    should be added to course.json.
    """
    picked = load_course().get("folder_names", {}).get(str(pid))
    if picked:
        return f"oj{pid}-{picked}"
    text = re.sub(r"[\[\]]", " ", name or "")
    slug = re.sub(r"[^A-Za-z0-9_\s-]", "", text)
    slug = re.sub(r"\s+", "_", slug.strip())
    slug = re.sub(r"_+", "_", slug).strip("_-")
    return f"oj{pid}-{slug}" if slug else f"oj{pid}"


def midterm_target(course84_id: int) -> int | None:
    """Course-78 problem id whose code answers a course-84 midterm problem."""
    target = load_course().get("midterm_course_map", {}).get(str(course84_id))
    return int(target) if target is not None else None
