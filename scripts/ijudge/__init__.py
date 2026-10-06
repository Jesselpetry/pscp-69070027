"""Shared helpers for the iJudge automation scripts on the OP branch.

    paths   -- where OP data and the main-branch problem folders live
    config  -- data/course.json: weeks, category tags, folder names, course ids
    code    -- the main.py template and stub detection
    auth    -- credential resolution + sign-in + session cookie caching
    weeks   -- week lookup for registry records, date formatting
    fsio    -- the dry-run-aware mutation layer (writes, renames, atomic JSON)
    client  -- retrying HTTP with session reuse and RSC helpers
    course  -- turning a raw iJudge problem record into our registry shape

Import as `from ijudge import ...`; the scripts add their own directory to
sys.path so this works without installation.
"""

from . import code, config, paths
from .auth import (
    CONFIG_FILE,
    AuthError,
    load_config,
    resolve_cookie,
    save_config,
    validate_cookie,
)
from .client import USER_AGENT, HttpError, fetch, fetch_problem_list
from .course import SUMMARY_FIELDS, build_problem_item, summary_fields
from .fsio import (
    ensure_dir,
    is_dry_run,
    rename_dir,
    safe_write_json,
    set_dry_run,
    write_text,
)
from .weeks import MONTH_NAMES, format_expire_date, get_week, release_of

__all__ = [
    "code", "config", "paths", "AuthError", "CONFIG_FILE", "load_config",
    "resolve_cookie", "save_config", "validate_cookie", "USER_AGENT",
    "HttpError", "fetch", "fetch_problem_list", "SUMMARY_FIELDS",
    "build_problem_item", "summary_fields", "ensure_dir", "is_dry_run",
    "rename_dir", "safe_write_json", "set_dry_run", "write_text",
    "MONTH_NAMES", "format_expire_date", "get_week", "release_of",
]
