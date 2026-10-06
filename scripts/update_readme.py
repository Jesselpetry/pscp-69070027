#!/usr/bin/env python3
"""Generate README.md on main from the summary registry and the folders on main.

Run from the repo root:  python3 .op/scripts/update_readme.py [--dry-run]
                                                               [--output PATH]
                                                               [--check]

Inputs are read-only: data/oj_problems.json (status, week, category flags),
data/course.json (week labels and titles), the problem folders on main and
recommended/. The README is the only file this script writes; refreshing the
registry is the scraper's job, so running this twice gives the same bytes.

A problem counts as passed when the registry says "Passed" or its oj/ folder
carries the ` ✅` suffix. Edit this script, not the README: manual edits are
overwritten.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.parse
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Iterable

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ijudge import code, config, fsio, paths  # noqa: E402

PASS_SUFFIX = " ✅"
LEGACY_BRANCH = "solutions/2026-s1"
OP_WORKTREE = ".op"
PLAN_REL = "docs/PLAN.md"
BRANCHES_HEADING = "## 🌿 Branches"

# Scripts documented in the README, in display order. Some are written by
# other changes; the links point at the OP branch, not at local files.
SCRIPTS = (
    ("pscp.py", "Single entry point: `python3 .op/scripts/pscp.py <command>` runs every script below."),
    ("scrape_all_oj_problems.py", "iJudge scraper: summary + detail registries, with a React Server Component (RSC) stream resolver."),
    ("render_problems.py", "Registry → `problem.md` for every problem + `main.py` stubs for new ones (offline, idempotent)."),
    ("update_readme.py", "Generates this README.md (only the README). Edit the script, not the README: manual edits are overwritten."),
    ("sync_oj_status.py", "Renames `oj/` folders to match the pass status (` ✅` suffix)."),
    ("check_repo.py", "Read-only consistency check (`doctor`): registry ↔ folders, weeks, Learning Logs, archived solutions."),
    ("archive_solutions.py", "Copies solved `main.py` files from main into `solutions/` on the OP branch."),
    ("run_samples.py", "Runs a problem's `main.py` against the official sample testcases."),
    ("submit_oj.py", "Submission CLI with session-cookie management and result polling."),
)

WORKFLOW = (
    ("scrape --fast", "refresh the problem list and status"),
    ("scrape --only <ids>", "fetch details of new problems"),
    ("render", "problem.md + main.py stubs on main"),
    ("test <id>", "run main.py against the official samples"),
    ("archive", "copy solved main.py into solutions/ (OP)"),
    ("readme", "regenerate this README"),
    ("doctor", "check that nothing is out of sync"),
)


@dataclass
class Problem:
    pid: int
    title: str
    week: int | None
    passed: bool
    learning_log: bool
    recommended: bool
    midterm: bool
    mini_exam: bool
    folder: str | None      # absolute path on main, if any
    rec_folder: str | None  # absolute path under recommended/, if any


# ---------------------------------------------------------------------------
# inputs
# ---------------------------------------------------------------------------

def load_registry() -> list[dict[str, Any]]:
    with open(paths.SUMMARY_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def count_records(path: str) -> int | None:
    """Number of records in a JSON registry, or None if it is missing."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return len(json.load(f))
    except (OSError, ValueError):
        return None


def index_recommended() -> dict[int, str]:
    found: dict[int, str] = {}
    if os.path.isdir(paths.RECOMMENDED_DIR):
        for d in sorted(os.listdir(paths.RECOMMENDED_DIR)):
            full = os.path.join(paths.RECOMMENDED_DIR, d)
            pid = paths.problem_id_of(d)
            if pid is not None and os.path.isdir(full):
                found.setdefault(pid, full)
    return found


def build_problems(registry: Iterable[dict[str, Any]]) -> list[Problem]:
    folders = paths.index_problem_dirs()
    rec = index_recommended()
    known = set()
    problems = []
    for item in sorted(registry, key=lambda r: r["id"]):
        pid = item["id"]
        known.add(pid)
        folder = folders.get(pid)
        week = item.get("week")
        if week is None:
            print(f"[WARN] oj{pid} has no week in the registry; run doctor", file=sys.stderr)
        problems.append(Problem(
            pid=pid,
            title=config.clean_title(item.get("name")) or f"oj{pid}",
            week=week,
            passed=item.get("status") == "Passed"
            or bool(folder and folder.endswith(PASS_SUFFIX)),
            learning_log=bool(item.get("is_learning_log")),
            recommended=bool(item.get("is_recommended")),
            midterm=bool(item.get("is_midterm")),
            mini_exam=bool(item.get("is_mini_exam")),
            folder=folder,
            rec_folder=rec.get(pid),
        ))
    orphans = sorted(set(folders) - known)
    if orphans:
        print(
            f"[WARN] {len(orphans)} folder(s) on main have no registry entry and are "
            f"left out: {', '.join(f'oj{p}' for p in orphans)}",
            file=sys.stderr,
        )
    return problems


# ---------------------------------------------------------------------------
# git (read-only)
# ---------------------------------------------------------------------------

def git_out(*args: str) -> str:
    """stdout of a read-only git command run in the OP worktree, "" on failure.

    The OP worktree shares refs with main, and unlike MAIN_ROOT it is always
    inside the repository (MAIN_ROOT may be overridden for testing).
    """
    try:
        return subprocess.check_output(
            ["git", "-C", paths.OP_ROOT, *args], stderr=subprocess.DEVNULL, text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def branch_exists(ref: str) -> bool:
    return bool(git_out("rev-parse", "--verify", "--quiet", ref))


@lru_cache(maxsize=None)
def github_repo() -> tuple[str, str] | None:
    """(owner, repo) of origin when it is on GitHub, over https or ssh."""
    url = git_out("remote", "get-url", "origin")
    m = re.match(
        r"^(?:https?://(?:[^@/]+@)?github\.com/|git@github\.com:|ssh://git@github\.com/)"
        r"([^/]+)/([^/]+?)(?:\.git)?/?$",
        url,
    )
    return (m.group(1), m.group(2)) if m else None


def op_link(path: str, label: str | None = None, *, directory: bool = False) -> str:
    """Markdown link to a file on the OP branch on GitHub, or a code span.

    These files are not on main, so a relative link would 404 on GitHub.
    """
    label = label or path
    repo = github_repo()
    if not repo:
        return f"`{label}`"
    kind = "tree" if directory else "blob"
    quoted = urllib.parse.quote(path.rstrip("/"))
    return f"[`{label}`](https://github.com/{repo[0]}/{repo[1]}/{kind}/{paths.OP_BRANCH}/{quoted})"


# ---------------------------------------------------------------------------
# formatting helpers
# ---------------------------------------------------------------------------

def rel(path: str) -> str:
    return os.path.relpath(path, paths.MAIN_ROOT).replace(os.sep, "/")


def md_link(path: str, label: str) -> str:
    return f"[`{label}`]({urllib.parse.quote(rel(path))})"


def file_link(folder: str | None, name: str) -> str:
    if folder and os.path.isfile(os.path.join(folder, name)):
        return md_link(os.path.join(folder, name), name)
    return "-"


def folder_link(folder: str | None) -> str:
    return md_link(folder, os.path.basename(folder)) if folder else "-"


def cell(text: str) -> str:
    return text.replace("|", "\\|")


def badge(p: Problem) -> str:
    return "✅ **Passed**" if p.passed else "🔄 *In Progress*"


def week_cell(week: int | None) -> str:
    return f"Week {week}" if week is not None else "-"


def pct(part: int, whole: int) -> float:
    return part / whole * 100 if whole else 0.0


def count_dirs(path: str, pattern: str = r"oj\d+.*") -> int:
    if not os.path.isdir(path):
        return 0
    return sum(
        1 for d in os.listdir(path)
        if re.fullmatch(pattern, d) and os.path.isdir(os.path.join(path, d))
    )


# ---------------------------------------------------------------------------
# sections
# ---------------------------------------------------------------------------

def header_lines() -> list[str]:
    return [
        '<div align="center">',
        '  <img src="public/IT-KMITL-Logo.png" alt="IT KMITL Logo" width="420"/>',
        "</div>",
        "",
        "---",
        "",
        "# PSCP — Problem Solving and Computer Programming",
        "",
        "**การแก้ปัญหาและการโปรแกรมคอมพิวเตอร์ (06066303)**",
        "3 Credits (2-2-5) · Bachelor's Degree · School of Information Technology, KMITL",
        "",
        "---",
        "",
        "## 👤 Student Information",
        "",
        "| Field | Details |",
        "| :--- | :---|",
        "| **Name (TH)** | นายฉัททัณฑ์ เพททริ |",
        "| **Name (EN)** | Chatan Petry |",
        "| **Student ID** | 69070027 |",
        "| **Email** | 69070027@kmitl.ac.th |",
        "| **Faculty** | คณะเทคโนโลยีสารสนเทศ (School of Information Technology) |",
        "| **Institution** | สถาบันเทคโนโลยีพระจอมเกล้าเจ้าคุณทหารลาดกระบัง (KMITL) |",
        "",
        "---",
        "",
    ]


def active_weeks(problems: list[Problem]) -> list[int]:
    return sorted({p.week for p in problems if p.week is not None})


def dashboard_lines(problems: list[Problem]) -> list[str]:
    total = len(problems)
    passed = sum(p.passed for p in problems)
    lines = [
        "## 📊 Overall Progress Dashboard",
        "",
        f"- **Total Problems Tracked**: `{total}`",
        f"- **✅ Solved / Passed**: `{passed}` ({pct(passed, total):.1f}%)",
        f"- **🔄 In Progress / Pending**: `{total - passed}`",
        "",
        "### 📅 Weekly Progress (นับตั้งแต่สัปดาห์แรกที่เปิดเทอม)",
        "",
        "| Week | Topic / Focus | Total | Passed | In Progress | Completion |",
        "| :---: | :--- | :---: | :---: | :---: | :---: |",
    ]
    for w in active_weeks(problems):
        rows = [p for p in problems if p.week == w]
        w_pass = sum(p.passed for p in rows)
        lines.append(
            f"| **Week {w}** | {config.week_title(w) or '-'} | {len(rows)} | {w_pass} "
            f"| {len(rows) - w_pass} | **{pct(w_pass, len(rows)):.1f}%** |"
        )
    lines += [
        "",
        "### 🏷️ Category Breakdown",
        "",
        "| Category | Total | Passed | In Progress |",
        "| :--- | :---: | :---: | :---: |",
    ]
    for label, rows in (
        ("🎯 Midterm Mock Exam", [p for p in problems if p.midterm]),
        ("📝 Mini Exam", [p for p in problems if p.mini_exam]),
        ("🌟 Recommended Problems", [p for p in problems if p.recommended]),
        ("📓 Learning Logs", [p for p in problems if p.learning_log]),
    ):
        done = sum(p.passed for p in rows)
        lines.append(f"| **{label}** | {len(rows)} | {done} | {len(rows) - done} |")
    lines += ["", "---", ""]
    return lines


def structure_lines(problems: list[Problem]) -> list[str]:
    oj_count = count_dirs(paths.OJ_DIR)
    ll_count = count_dirs(paths.MAIN_ROOT, r"oj\d+")
    rec_count = count_dirs(paths.RECOMMENDED_DIR)
    scripts_dir = os.path.join(paths.OP_ROOT, "scripts")
    script_count = (
        sum(1 for f in os.listdir(scripts_dir) if f.endswith(".py"))
        if os.path.isdir(scripts_dir) else 0
    )
    solution_count = count_dirs(paths.SOLUTIONS_DIR, r"oj\d+")
    detail_count = count_records(paths.DETAIL_JSON)
    detail = f" ({detail_count} ข้อ)" if detail_count is not None else ""
    tree = [
        ("pscp-69070027/", "branch main — โจทย์ + โค้ดของตัวเอง"),
        ("├── oj/", f"โจทย์ปกติ + Midterm + Mini Exam ({oj_count} โฟลเดอร์): oj<id>-<Name>/ → problem.md, main.py (ลงท้าย ✅ = ผ่านแล้ว)"),
        ("├── oj<id>/", f"Learning Log ({ll_count} โฟลเดอร์): main.py, problem.md, submission.md (+ ai_reflection.md)"),
        ("├── recommended/", f"สรุปโจทย์แนะนำที่เขียนเอง ({rec_count} ข้อ) + สรุป ce-kmitl"),
        ("├── AI-Guidelines-PSCP/", "แนวทางการใช้ AI ของรายวิชา"),
        ("├── public/", "รูปประกอบ README"),
        ("├── README.md", "generated โดย update_readme.py — ห้ามแก้มือ"),
        ("├── CONTRIBUTE.md", "วิธีเพิ่มโจทย์และส่งงาน"),
        (f"└── {OP_WORKTREE}/", f"worktree ของ branch {paths.OP_BRANCH} (gitignored บน main)"),
        ("    ├── scripts/", f"{script_count} scripts + ijudge/ (shared package)"),
        ("    ├── data/", f"course.json, oj_problems.json ({len(problems)} ข้อ), all_problems_detail.json{detail}, html_cache/ (gitignored)"),
        ("    ├── solutions/", f"เฉลยครบ {solution_count} ข้อ: oj<id>/main.py"),
        ("    └── docs/", "PLAN.md"),
    ]
    width = max(len(entry) for entry, _ in tree) + 2
    return [
        "## 📁 Repository Structure",
        "",
        "```",
        *(f"{entry.ljust(width)}# {note}" for entry, note in tree),
        "```",
        "",
        "---",
        "",
    ]


def branch_lines() -> list[str]:
    """Branch table from local refs; regenerate after committing to refresh it."""
    branches = [
        (paths.MAIN_BRANCH, "โจทย์ + โค้ดของตัวเอง"),
        (paths.OP_BRANCH, "scripts + data + เฉลยครบใน `solutions/`"),
    ]
    present = [(b, role) for b, role in branches if branch_exists(b)]
    lines = [BRANCHES_HEADING, ""]
    if present:
        counts = git_out(
            "rev-list", "--left-right", "--count", f"{paths.MAIN_BRANCH}...{paths.OP_BRANCH}"
        ).split()
        ahead_behind = {}
        if len(present) == 2 and len(counts) == 2:
            ahead_behind = {
                paths.MAIN_BRANCH: f"{counts[0]} / {counts[1]}",
                paths.OP_BRANCH: f"{counts[1]} / {counts[0]}",
            }
        lines += [
            "| Branch | บทบาท | Commit ล่าสุด | นำ / ตาม อีก branch | ยังไม่ push |",
            "| :--- | :--- | :--- | :---: | :---: |",
        ]
        for branch, role in present:
            last = git_out("log", "-1", "--format=%h · %cs", branch) or "-"
            sha, _, date = last.partition(" · ")
            commit = f"`{sha}` · {date}" if date else "-"
            unpushed = (
                git_out("rev-list", "--count", f"origin/{branch}..{branch}") or "-"
                if branch_exists(f"origin/{branch}") else "-"
            )
            lines.append(
                f"| `{branch}` | {role} | {commit} | {ahead_behind.get(branch, '-')} | {unpushed} |"
            )
        lines.append("")
    if branch_exists(LEGACY_BRANCH):
        lines += [
            f"> `{LEGACY_BRANCH}` เป็น branch เก่า — ถูกแทนที่ด้วย `{paths.OP_BRANCH}` "
            f"(`solutions/`) แล้ว ลบได้เมื่อตรวจว่าโค้ดครบ",
            "",
        ]
    setup = [
        (f"git worktree add {OP_WORKTREE} {paths.OP_BRANCH}", "ครั้งเดียว ถ้ายังไม่มี"),
        (f"python3 {OP_WORKTREE}/scripts/pscp.py readme", "รัน script จาก root ของ repo"),
    ]
    width = max(len(cmd) for cmd, _ in setup) + 3
    lines += [
        "```bash",
        *(f"{cmd.ljust(width)}# {note}" for cmd, note in setup),
        "```",
        "",
        "---",
        "",
    ]
    return lines


def midterm_lines(problems: list[Problem]) -> list[str]:
    rows = [p for p in problems if p.midterm]
    weeks = sorted({p.week for p in rows if p.week is not None})
    suffix = f" ({', '.join(f'Week {w}' for w in weeks)})" if weeks else ""
    lines = [
        f"## 🎯 1. Midterm Mock Exam Problems{suffix}",
        "",
        "ชุดข้อสอบจำลอง Midterm PSCP พร้อมคำอธิบายโจทย์ ข้อกำหนด และตัวอย่างเทสเคส",
        "",
        "| OJ ID | Problem Name | Status | Problem Folder | Problem Spec | Solution Code |",
        "| :---: | :--- | :---: | :--- | :---: | :---: |",
    ]
    for p in rows:
        lines.append(
            f"| **{p.pid}** | {cell(p.title)} | {badge(p)} | {folder_link(p.folder)} "
            f"| {file_link(p.folder, 'problem.md')} | {file_link(p.folder, 'main.py')} |"
        )
    return lines + ["", "---", ""]


def recommended_lines(problems: list[Problem]) -> list[str]:
    rows = [p for p in problems if p.recommended]
    lines = [
        f"## 🌟 2. Recommended Problems (คลังโจทย์แนะนำ {len(rows)} ข้อ)",
        "",
        f"โจทย์สำคัญ {len(rows)} ข้อที่รวบรวมเทคนิคสำคัญของภาษา Python พร้อมคำอธิบายและแนวคิดอย่างละเอียด",
        "",
        "| OJ ID | Problem Name | Week | Status | Recommended Folder | Standard Folder | Problem Spec | Solution Code |",
        "| :---: | :--- | :---: | :---: | :--- | :--- | :---: | :---: |",
    ]
    for p in rows:
        lines.append(
            f"| **{p.pid}** | {cell(p.title)} | {week_cell(p.week)} | {badge(p)} "
            f"| {folder_link(p.rec_folder)} | {folder_link(p.folder)} "
            f"| {file_link(p.rec_folder, 'problem.md')} | {file_link(p.rec_folder, 'main.py')} |"
        )
    return lines + ["", "---", ""]


def learning_log_lines(problems: list[Problem]) -> list[str]:
    lines = [
        "## 📓 3. Learning Logs (บันทึกการเรียนรู้)",
        "",
        "โจทย์ที่ต้องส่ง Learning Log พร้อมบันทึก `submission.md` และการสะท้อนความคิด",
        "",
        "| OJ ID | Problem Name | Week | Status | Learning Log Folder | Problem Spec | Submission Doc | Code |",
        "| :---: | :--- | :---: | :---: | :--- | :---: | :---: | :---: |",
    ]
    for p in problems:
        if not p.learning_log:
            continue
        lines.append(
            f"| **{p.pid}** | {cell(p.title)} | {week_cell(p.week)} | {badge(p)} "
            f"| {folder_link(p.folder)} | {file_link(p.folder, 'problem.md')} "
            f"| {file_link(p.folder, 'submission.md')} | {file_link(p.folder, 'main.py')} |"
        )
    return lines + ["", "---", ""]


def weekly_lines(problems: list[Problem]) -> list[str]:
    lines = ["## 💻 4. Standard OJ Problems (จำแนกตามสัปดาห์ตั้งแต่เปิดเทอม)", ""]
    for w in active_weeks(problems):
        rows = [p for p in problems if p.week == w and not p.learning_log]
        if not rows:
            continue
        done = sum(p.passed for p in rows)
        title = config.week_title(w)
        heading = f"{config.week_label(w)}: {title}" if title else config.week_label(w)
        lines += [
            f"### 📅 {heading}",
            "",
            f"> รวม `{len(rows)}` ข้อ (ผ่านแล้ว `{done}/{len(rows)}`)",
            "",
            "| OJ ID | Problem Name | Status | Folder Link | Problem Spec | Solution Code |",
            "| :---: | :--- | :---: | :--- | :---: | :---: |",
        ]
        for p in rows:
            lines.append(
                f"| **{p.pid}** | {cell(p.title)} | {badge(p)} | {folder_link(p.folder)} "
                f"| {file_link(p.folder, 'problem.md')} | {file_link(p.folder, 'main.py')} |"
            )
        lines.append("")
    return lines + ["---", ""]


def automation_lines(problems: list[Problem]) -> list[str]:
    detail_count = count_records(paths.DETAIL_JSON)
    detail = f" ({detail_count} problems)" if detail_count is not None else ""
    solution_count = count_dirs(paths.SOLUTIONS_DIR, r"oj\d+")
    lines = [
        "## 🛠️ Data & Automation Scripts",
        "",
        f"ไฟล์ทั้งหมดในหัวข้อนี้อยู่บน branch `{paths.OP_BRANCH}` (worktree `{OP_WORKTREE}/`) ไม่ใช่ `{paths.MAIN_BRANCH}`",
        "",
        f"- {op_link('data/course.json')} — Course config: week windows (release dates), week titles, category tags, folder names, midterm map. Adding a week = one entry here.",
        f"- {op_link('data/oj_problems.json')} — Summary registry ({len(problems)} problems): id, week, status, pass stats, deadline, release date, and category flags.",
        f"- {op_link('data/all_problems_detail.json')} — Detail registry{detail}: problem statements, input/output specifications, time/memory limits, and sample testcases.",
        f"- {op_link('solutions/', directory=True)} — Archived reference code ({solution_count} problems): `solutions/oj<id>/main.py`.",
    ]
    for name, desc in SCRIPTS:
        lines.append(f"- {op_link(f'scripts/{name}')} — {desc}")
    lines.append(f"- {op_link('scripts/README.md')} — Setup, credentials, and every command option.")
    lines += ["", "### 🔁 Weekly Workflow", "", "```bash"]
    width = max(len(cmd) for cmd, _ in WORKFLOW)
    for cmd, note in WORKFLOW:
        lines.append(f"python3 {OP_WORKTREE}/scripts/pscp.py {cmd.ljust(width)}   # {note}")
    lines += ["```", ""]
    if os.path.isfile(os.path.join(paths.OP_ROOT, PLAN_REL)):
        lines += [
            "### 🗺️ Roadmap",
            "",
            f"แผนจัดระเบียบ repo และขั้นตอนแต่ละ phase อยู่ที่ {op_link(PLAN_REL)} บน branch `{paths.OP_BRANCH}`",
            "",
        ]
    return lines + ["---", ""]


def style_lines() -> list[str]:
    stub = code.stub_solution("Problem Name").rstrip("\n").split("\n")
    return [
        "## 🐍 Code Style Guidelines",
        "",
        "All Python solutions follow strict PEP-8 standards with docstrings:",
        "",
        "```python",
        *stub,
        "```",
        "",
    ]


def generate(problems: list[Problem]) -> str:
    lines = (
        header_lines()
        + dashboard_lines(problems)
        + structure_lines(problems)
        + branch_lines()
        + midterm_lines(problems)
        + recommended_lines(problems)
        + learning_log_lines(problems)
        + weekly_lines(problems)
        + automation_lines(problems)
        + style_lines()
    )
    return "\n".join(lines).strip() + "\n"


def without_branches(text: str) -> str:
    """README text minus the Branches section.

    That section reports the commit that contains the README itself, so it
    can never be current right after a commit; --check ignores it.
    """
    return re.sub(rf"{re.escape(BRANCHES_HEADING)}\n.*?\n---\n", "", text, flags=re.S)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Regenerate README.md on main from the registry and the problem folders."
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Report what would be written, write nothing.")
    parser.add_argument("--output", metavar="PATH",
                        help=f"Write here instead of {paths.README_PATH}.")
    parser.add_argument("--check", action="store_true",
                        help="Exit 1 if the README is out of date (ignores the Branches section); write nothing.")
    args = parser.parse_args()
    fsio.set_dry_run(args.dry_run)

    if not os.path.isfile(paths.SUMMARY_JSON):
        print(f"Error: {paths.SUMMARY_JSON} not found. Run the scraper first.", file=sys.stderr)
        return 2
    problems = build_problems(load_registry())
    content = generate(problems)
    target = os.path.abspath(args.output) if args.output else paths.README_PATH

    current = None
    if os.path.isfile(target):
        with open(target, "r", encoding="utf-8") as f:
            current = f.read()

    passed = sum(p.passed for p in problems)
    summary = f"{len(problems)} problems, {passed} passed"
    if args.check:
        if current is not None and without_branches(current) == without_branches(content):
            print(f"{target} is up to date ({summary}).")
            return 0
        print(f"{target} is out of date; run update_readme.py.", file=sys.stderr)
        return 1
    if current == content:
        print(f"{target} unchanged ({summary}).")
        return 0
    fsio.write_text(target, content)
    if not fsio.is_dry_run():
        print(f"Wrote {target} ({content.count(chr(10))} lines, {summary}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
