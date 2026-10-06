"""Where everything lives, resolved once.

The scripts run from the OP branch, checked out as the worktree `.op/` inside
the main checkout, and work on two trees:

    OP_ROOT    this worktree: scripts/, data/, solutions/, docs/
    MAIN_ROOT  the main branch checkout: oj/, oj<id>/, recommended/, README.md

MAIN_ROOT is $PSCP_MAIN_ROOT when set, else the worktree that has `main`
checked out (from `git worktree list`), else the directory containing OP_ROOT.
"""

from __future__ import annotations

import os
import re
import subprocess

OP_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MAIN_BRANCH = "main"
OP_BRANCH = "OP"
OP_WORKTREE_NAME = ".op"


def _main_from_git() -> str | None:
    """Path of the worktree that has MAIN_BRANCH checked out, if any."""
    try:
        out = subprocess.check_output(
            ["git", "-C", OP_ROOT, "worktree", "list", "--porcelain"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    path = None
    for line in out.splitlines():
        if line.startswith("worktree "):
            path = line[len("worktree "):]
        elif line == f"branch refs/heads/{MAIN_BRANCH}" and path:
            return path
    return None


def _resolve_main_root() -> str:
    env = os.environ.get("PSCP_MAIN_ROOT")
    if env:
        return os.path.abspath(os.path.expanduser(env))
    return _main_from_git() or os.path.dirname(OP_ROOT)


MAIN_ROOT = _resolve_main_root()

# OP branch: data, archive, tooling state.
DATA_DIR = os.path.join(OP_ROOT, "data")
COURSE_CONFIG = os.path.join(DATA_DIR, "course.json")
SUMMARY_JSON = os.path.join(DATA_DIR, "oj_problems.json")
DETAIL_JSON = os.path.join(DATA_DIR, "all_problems_detail.json")
COURSE_84_JSON = os.path.join(DATA_DIR, "course_84_problems.json")
HTML_CACHE_DIR = os.path.join(DATA_DIR, "html_cache")
SOLUTIONS_DIR = os.path.join(OP_ROOT, "solutions")
CONFIG_FILE = os.path.join(OP_ROOT, "submit_config.json")

# main branch: the student's own work.
OJ_DIR = os.path.join(MAIN_ROOT, "oj")
RECOMMENDED_DIR = os.path.join(MAIN_ROOT, "recommended")
README_PATH = os.path.join(MAIN_ROOT, "README.md")

# "oj3381" (Learning Log), "oj3290-Left_Arrow", "oj3290-Left_Arrow ✅"
_PROBLEM_DIR_RE = re.compile(r"^oj(\d+)(?:[- ].*)?$")


def problem_id_of(dirname: str) -> int | None:
    """Problem id encoded in a problem folder name, or None."""
    m = _PROBLEM_DIR_RE.match(dirname)
    return int(m.group(1)) if m else None


def index_problem_dirs() -> dict[int, str]:
    """Map problem id -> its folder on main.

    Learning Logs live at the root as `oj<id>/`, everything else under `oj/`.
    A root folder wins if both exist, matching where the scraper writes.
    """
    found: dict[int, str] = {}
    if os.path.isdir(OJ_DIR):
        for d in sorted(os.listdir(OJ_DIR)):
            pid = problem_id_of(d)
            full = os.path.join(OJ_DIR, d)
            if pid is not None and os.path.isdir(full):
                found.setdefault(pid, full)
    if os.path.isdir(MAIN_ROOT):
        for d in sorted(os.listdir(MAIN_ROOT)):
            full = os.path.join(MAIN_ROOT, d)
            if re.fullmatch(r"oj\d+", d) and os.path.isdir(full):
                found[int(d[2:])] = full
    return found


def find_problem_dir(pid: int) -> str | None:
    """Existing folder for one problem on main, or None."""
    return index_problem_dirs().get(pid)


def solution_file(pid: int) -> str:
    """Archived reference solution for a problem (may not exist yet)."""
    return os.path.join(SOLUTIONS_DIR, f"oj{pid}", "main.py")
