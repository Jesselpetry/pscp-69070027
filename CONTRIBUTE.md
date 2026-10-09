# CONTRIBUTE.md (OP) — Agent Operations Guide

**Single source of truth for an AI agent working on this repository.** Read
this top to bottom once; it tells you everything needed to take a problem from
"new on iJudge" to "passed, archived, committed, and live on ihelp" without
guessing.

Companion docs:
- Root [`../CONTRIBUTE.md`](../CONTRIBUTE.md) — Thai quick-start for the human (same pipeline, fewer internals).
- [`scripts/README.md`](scripts/README.md) — tooling reference (command flags, data files, write rules).
- [`README.md`](README.md) — one-paragraph pointer to the OP branch.

---

## Table of contents

1. [Golden rules](#1-golden-rules)
2. [Architecture — two branches, one worktree](#2-architecture--two-branches-one-worktree)
3. [Environment setup](#3-environment-setup)
4. [Authentication (iJudge session)](#4-authentication-ijudge-session)
5. [Command reference](#5-command-reference)
6. [Fast-Track pipeline (new problem → done)](#6-fast-track-pipeline-new-problem--done)
7. [Code conventions & scoring](#7-code-conventions--scoring)
8. [Folder & naming conventions](#8-folder--naming-conventions)
9. [Data files — who edits what](#9-data-files--who-edits-what)
10. [What the scripts may and may not write](#10-what-the-scripts-may-and-may-not-write)
11. [Learning Logs](#11-learning-logs)
12. [Config edits (new week, Thai titles)](#12-config-edits-new-week-thai-titles)
13. [Verification](#13-verification)
14. [Commit & push (both branches)](#14-commit--push-both-branches)
15. [Downstream: rebuild the ihelp registry](#15-downstream-rebuild-the-ihelp-registry)
16. [Agent safety rails](#16-agent-safety-rails)

---

## 1. Golden rules

Read these before touching anything.

- **Two branches, two jobs.** `main` holds the student's own work; `OP` holds the
  tooling, data, and reference solutions. They are different git histories in the
  same directory tree (OP is a worktree at `.op/`). Commit and push each one
  separately. See [§2](#2-architecture--two-branches-one-worktree).
- **`main` keeps empty stubs.** The student's `oj/.../main.py` is hand-written. Do
  **not** seed it with iJudge code. Reference solutions live only on OP under
  `solutions/oj<id>/main.py`.
- **Everything runs through `pscp.py`** from the repo root:
  `python3 .op/scripts/pscp.py <command>`. Don't call the underlying scripts
  directly.
- **Preview before you write.** Every writing command takes `--dry-run`. Use it
  when unsure.
- **Never commit secrets.** `submit_config.json` and `.env` are gitignored and
  hold the iJudge token. Do not add, print, or paste them anywhere.
- **Submitting to iJudge is an outward-facing action.** It uses the student's real
  account. Don't bulk-submit speculatively; confirm the target ids first, and
  throttle bulk runs ([§4](#4-authentication-ijudge-session)).
- **After solutions change, the ihelp site is stale** until you rebuild its
  registry ([§15](#15-downstream-rebuild-the-ihelp-registry)).

---

## 2. Architecture — two branches, one worktree

| Tree | Checked out at | Branch | Holds |
|---|---|---|---|
| `main` | repo root | `main` | `oj/oj<id>-<Name>[ ✅]/`, Learning Logs `oj<id>/`, `recommended/`, `README.md`, root `CONTRIBUTE.md` |
| `OP` | `.op/` | `OP` | `scripts/`, `data/`, `solutions/`, `docs/`, this file |

`.op/` is a **git worktree** of the `OP` branch and is gitignored on `main`, so
from `main`'s point of view it does not exist. Running `git status` at the root
shows only `main`; running `git -C .op status` shows `OP`.

- `scripts/ijudge/paths.py` locates the `main` checkout via `git worktree list`.
- Override with `PSCP_MAIN_ROOT` (the test suite points it at a fixture).
- `PSCP_OP_ROOT` lets external consumers (ihelp) point at this OP tree.

The split means: a finished problem touches **both** trees — the student code and
the ` ✅` suffix on `main`, the archived copy and updated registry on `OP`.

---

## 3. Environment setup

One-time, from the `main` checkout:

```bash
git worktree add .op OP
pip install -r .op/scripts/requirements.txt
```

Python 3 with `requests` (see `scripts/requirements.txt`). All commands are run
from the repo root unless noted.

---

## 4. Authentication (iJudge session)

Commands that hit iJudge (`scrape`, `submit`, `web`) need a session.
`ijudge/auth.py::resolve_cookie` finds one automatically, in this order:

1. `IJUDGE_COOKIE` env var (if not expired).
2. Cached `cookie` token in `.op/submit_config.json` (if not expired).
3. **Auto-refresh**: fresh `access_token` pulled from a local browser profile
   (Zen/Firefox `cookies.sqlite`) via `find_browser_cookie()`.
4. Sign-in with `IJUDGE_USER` / `IJUDGE_PASS`.

**Normally you set nothing** — if iJudge is open in Zen Browser, step 3 supplies
the cookie. Verify the session without submitting:

```bash
python3 .op/scripts/pscp.py submit --dry-run --ids 3599   # previews plan, proves auth works
```

Manual override (Zen closed, or a different browser):

```bash
python3 .op/scripts/pscp.py submit --set-cookie     # paste & save interactively
export IJUDGE_COOKIE='access_token=...'              # or via env; DevTools > Network > Cookie header, ~24h life
export IJUDGE_USER=... IJUDGE_PASS=...               # or let the tool mint one
```

The token is cached in `submit_config.json` (gitignored). A password, if used,
mints a token once and is never stored.

**Rate-limit etiquette.** `submit` with `--yes` sends immediately. For bulk runs
spread them out so you don't hammer iJudge:

```bash
python3 .op/scripts/pscp.py submit --week 14 --yes --delay-range 4-6m
```

---

## 5. Command reference

One entry point, run from the repo root:

```bash
python3 .op/scripts/pscp.py <command> [options]
python3 .op/scripts/pscp.py <command> --help   # the underlying script's own flags
```

| Command | Does | Network | Key flags |
|---|---|:---:|---|
| `scrape` | iJudge → `data/*.json`, then renders fetched problems onto `main` | yes | `--fast` (summary registry only, one request), `--only 3290-3301`, `--seed-code` (replace untouched stubs with iJudge code — off by default), `--dry-run` |
| `render` | `data/` → problem folders on `main` (`problem.md`, `main.py` stub, ✅ sync); offline | no | `--only IDS`, `--check` (exit 1 if anything would change), `--dry-run` |
| `status` | add/remove ` ✅` on `oj/` folders to match the registry | no | `--dry-run` |
| `test` | run `main.py` against the official samples | no | positional `ids`/ranges, `--week N` (repeatable), `--solutions` (test the archived copy) |
| `submit` | submit code from `main` to iJudge | yes | `--ids`, `--week`, `--all`, `--midterm`, `--yes`, `--dry-run`, `--include-learning-log`, `--set-cookie`, `--delay-range` |
| `archive` | copy solved `main.py` from `main` into `solutions/` | no | `--ids`, `--update` (overwrite drift), `--restore IDS` (archive → main stub), `--blank IDS` (reset main to stub), `--dry-run` |
| `readme` | regenerate `README.md` on `main` | no | `--check`, `--output PATH`, `--dry-run` |
| `doctor` | consistency report: registry ↔ folders, ✅ vs status, archive drift, missing `submission.md` | no | `--quiet` |
| `web` | local dashboard at `http://127.0.0.1:8765` | yes | `--port`, `--no-browser` |

Every writing command accepts `--dry-run`. On `scrape`, `--dry-run` still fetches;
only the writes are suppressed.

---

## 6. Fast-Track pipeline (new problem → done)

Given a new problem (iJudge link, OJ id, or statement), do this in order:

```
[1 Check auth] → [2 Config course.json] → [3 Scrape & render] → [4 Solve]
                                                                     │
[8 Commit & push] ← [7 Post-pass sync] ← [6 Submit] ← [5 Test & lint]
```

**1. Check auth** — see [§4](#4-authentication-ijudge-session). Usually a no-op.

**2. Config `course.json` first** (only if needed) — see
[§12](#12-config-edits-new-week-thai-titles). Needed when the title is Thai (add a
`folder_names` entry) or the problem is in a new teaching week (add a `weeks`
entry). Do this **before** scrape/render so the folder is named right on creation.

**3. Scrape & render:**

```bash
python3 .op/scripts/pscp.py scrape --only <ids>   # e.g. 3599,3600 or 3586-3598
```

Creates `oj/oj<id>-<Name>/problem.md` and an empty `main.py` stub on `main`.

**4. Solve** — write the student's logic in `oj/oj<id>-<Name>/main.py` following
[§7](#7-code-conventions--scoring).

**5. Test & lint:**

```bash
python3 .op/scripts/pscp.py test <id>
flake8 "oj/oj<id>-<Name>/main.py"
```

All samples must `PASS` and flake8 must be clean before submitting.

**6. Submit:**

```bash
python3 .op/scripts/pscp.py submit --ids <ids> --yes
```

Target verdict: `✅ PPPP…` (all `P`), Score `1000.0 / 1000.0`, PEP8 `10.0 / 10.0`.

**7. Post-pass sync** (one line):

```bash
python3 .op/scripts/pscp.py status && \
python3 .op/scripts/pscp.py archive && \
python3 .op/scripts/pscp.py readme && \
python3 .op/scripts/pscp.py doctor
```

| Step | Effect |
|---|---|
| `status` | appends ` ✅` to passed folders, e.g. `oj/oj3599-SumOfNumber ✅/` |
| `archive` | copies passed `main.py` → `solutions/oj<id>/main.py` on OP |
| `readme` | rebuilds the stats tables in `main`'s `README.md` |
| `doctor` | consistency check — must end with `== Errors: none ==` |

**8. Commit & push both branches** — see [§14](#14-commit--push-both-branches).
Then rebuild ihelp ([§15](#15-downstream-rebuild-the-ihelp-registry)).

---

## 7. Code conventions & scoring

Scoring on iJudge is **Score `/1000.0`** (all sample groups correct) plus **PEP8
`/10.0`**. A perfect result is all-`P` verdict + `1000.0` + `10.0`.

Standard shape for `oj/oj<id>-<Name>/main.py`:

```python
""" Problem Name """


def main():
    """Problem Name"""
    # solution logic here


if __name__ == "__main__":
    main()
```

PEP8 rules that earn the full `10.0`:

- Module docstring on line 1.
- All logic inside `def main():`, with a function docstring as its first line.
- Two blank lines between `def main():` and the `if __name__ == "__main__":` guard.
- Lines ≤ 79 characters.
- No trailing whitespace.
- No unused imports or variables.

Verify with `flake8` before every submit.

---

## 8. Folder & naming conventions

| Kind | Path | Example |
|---|---|---|
| Normal / Midterm / Mini Exam problem | `oj/oj<id>-<Name>/` | `oj/oj3599-SumOfNumber/` |
| Passed problem | same, with ` ✅` suffix | `oj/oj3599-SumOfNumber ✅/` |
| Learning Log | `oj<id>/` at repo root (no ✅) | `oj2996/` |

The ` ✅` suffix is managed only by `status`; never rename folders by hand.

---

## 9. Data files — who edits what

All under `.op/data/` on OP:

| File | Edited by | Holds |
|---|---|---|
| `course.json` | **you** | `course_ids`, `weeks` (windows by release date), `week_overrides`, `categories`, `folder_names`, `midterm_course_map`, `semester`, `utc_offset_hours` |
| `oj_problems.json` | `scrape` | summary registry: id, name, week, status, stats, deadline, `released`, category flags |
| `all_problems_detail.json` | `scrape` | statement, I/O spec, limits, sample cases, last submitted code |
| `course_84_problems.json` | you | midterm problems of course 84 |
| `html_cache/` | `scrape` | raw pages for parser debugging (gitignored) |
| `solutions/oj<id>/main.py` | `archive` | finished reference code, keyed by id |

`course.json` is the only data file you hand-edit. The rest are generated.

---

## 10. What the scripts may and may not write

| File | Rule |
|---|---|
| `problem.md` | rewritten only if generated (marker comment or the legacy `## 1. โจทย์จริงจาก iJudge` heading) |
| `main.py` on `main` | created once as a stub; later only an **untouched** stub is refreshed (`ijudge.code.is_stub`). Hand-written code is never overwritten unless you pass `--seed-code` (don't, on `main`) |
| `submission.md`, `ai_reflection.md`, `recommended/` | **never** touched |
| folder names | only the ` ✅` suffix, only under `oj/` |

This is why it is safe to re-run `scrape`/`render`: student code and notes are
preserved.

---

## 11. Learning Logs

Problems tagged `[LEARNING LOG]`:

1. Folder lives at the repo **root** as `oj<id>/` (not under `oj/`), no ✅ suffix.
2. Must carry hand-written docs:
   - `submission.md` — the learning write-up (from the course template).
   - `ai_reflection.md` — AI-use note, when AI was used.
3. `submit` **excludes** Learning Logs by default (prevents re-submission). To
   include them explicitly: `submit --ids <id> --include-learning-log`.
4. `doctor` warns about a Learning Log missing `submission.md`.

Agents do not write `submission.md` / `ai_reflection.md` — those are the student's.

---

## 12. Config edits (new week, Thai titles)

Edit [`data/course.json`](data/course.json), then re-run `render` (or `scrape`).

**New teaching week** — add one entry to `weeks`:

```json
{"week": 14, "from": "2026-10-09", "title": "ชุดข้อสอบย่อยจำลอง (Mini Exam / Mock Test)"}
```

A week runs from its `from` date to the next entry's `from` (the last one lasts 7
days), in Bangkok time (`utc_offset_hours`). A problem released outside every
window keeps its stored week and `doctor` warns. Mini Exams are placed in the week
set by `categories.mini_exam.week` — move that number before a real week 14
arrives.

**Thai title** — new folders take an ASCII name from the title; a Thai-only title
yields a bare `oj<id>`. Add an English name to `folder_names` **before** the folder
is created:

```json
"folder_names": { "3600": "Calories" }
```

Then `render` again (or rename the folder by hand if it already exists).

---

## 13. Verification

```bash
python3 .op/scripts/pscp.py test <id|range|--week N>   # samples against main
python3 .op/scripts/pscp.py test <id> --solutions      # samples against the archived copy
python3 .op/scripts/pscp.py doctor                     # must say "== Errors: none =="
flake8 "oj/oj<id>-<Name>/main.py"                       # PEP8
```

`doctor` reports **Errors** (block the other scripts, exit 1) and **Warnings**
(drift a routine run repairs). Investigate every Error before committing.

Unit tests for the tooling itself (OP):

```bash
python3 -m unittest discover -s .op/scripts/tests -t .op/scripts
```

---

## 14. Commit & push (both branches)

The trees have separate histories; commit each.

```bash
# main — student code, ✅ suffixes, regenerated README
git add -A
git commit -m "feat(oj): complete Week <W> problems <ids>, update README"
git push origin main

# OP — archived solutions, updated registries
git -C .op add -A
git -C .op commit -m "feat(solutions): add <ids> solutions and course data"
git -C .op push origin OP
```

Conventional-commit scopes used here: `feat(oj)`, `feat(solutions)`,
`feat(scripts)`, `docs(readme)`, `docs`, `chore`. End agent-authored commits with:

```
Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
```

Keep unrelated generated changes (e.g. a stray `scrape` refresh of
`oj_problems.json`) out of a solution commit — stage deliberately, don't blanket
`add -A` across unrelated work.

---

## 15. Downstream: rebuild the ihelp registry

The ihelp website is a **separate repo** at
`/Users/chatan/Desktop/Keep/KMITL/IT-KMITL/ihelp` (branch `main`). It serves a
pre-built `data/pscp/problems.json` from this OP tree's `solutions/` and `data/`.
After **any** solution or registry change, that JSON is stale until rebuilt:

```bash
cd /Users/chatan/Desktop/Keep/KMITL/IT-KMITL/ihelp
python3 scripts/build_pscp_registry.py
python3 scripts/build_pscp_edge_cases.py
git add data/pscp/problems.json && git commit -m "chore(pscp): rebuild registry" && git push origin main
```

Its scripts already point at `.op/solutions` (`PSCP_OP_ROOT` overrides the path).
Skip this and the site shows empty stubs / stale tags.

> Note: `main`'s `README.md` tracks the *student's* pass progress (not everything
> is submitted). OP `solutions/` is the complete reference set — these two counts
> differ on purpose.

---

## 16. Agent safety rails

- **Confirm the id set** before `submit`; it posts to the student's real iJudge
  account. Prefer `--dry-run` first.
- **Don't `--seed-code` on `main`** — it would replace the student's stubs with
  iJudge code. Reference code belongs on OP via `archive`.
- **Don't touch** `submission.md`, `ai_reflection.md`, or `recommended/`.
- **Don't commit** `submit_config.json`, `.env`, or any `access_token`.
- **Run `doctor`** after structural changes and resolve every Error.
- **Rebuild ihelp** after solutions change, or the site goes stale.
- When a change spans both trees, push `main` and `OP` separately and keep each
  commit scoped to its own work.
