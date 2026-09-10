"""Shared helpers for the iJudge automation scripts.

Everything that was previously copy-pasted between scrape_all_oj_problems.py,
sync_oj_problems.py (x2) and update_readme.py lives here exactly once:

    auth    -- credential resolution + sign-in + session cookie caching
    weeks   -- the course-week classifier and date formatting
    fsio    -- the dry-run-aware mutation layer (writes, renames, atomic JSON)
    http    -- retrying HTTP with session reuse and RSC helpers
    course  -- turning a raw iJudge problem record into our registry shape

Import as `from ijudge import ...`; the scripts add their own directory to
sys.path so this works without installation.
"""

from .auth import (
    CONFIG_FILE,
    AuthError,
    load_config,
    resolve_cookie,
    save_config,
    validate_cookie,
)
from .course import build_problem_item, summary_fields
from .fsio import (
    ensure_dir,
    is_dry_run,
    rename_dir,
    safe_write_json,
    set_dry_run,
    write_text,
)
from .client import USER_AGENT, HttpError, fetch, fetch_problem_list
from .weeks import MONTH_NAMES, format_expire_date, get_week

__all__ = [
    "AuthError", "CONFIG_FILE", "load_config", "resolve_cookie", "save_config",
    "validate_cookie", "build_problem_item", "summary_fields", "ensure_dir",
    "is_dry_run", "rename_dir", "safe_write_json", "set_dry_run", "write_text",
    "USER_AGENT", "HttpError", "fetch", "fetch_problem_list", "MONTH_NAMES",
    "format_expire_date", "get_week",
]
