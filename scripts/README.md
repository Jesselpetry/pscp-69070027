# scripts/

Automation for the PSCP archive: fetch problems from iJudge, render the
problem folders on `main`, check and archive solutions, regenerate the README.

These scripts live on the `OP` branch and work on two checkouts at once:

| Tree | Where | Holds |
|---|---|---|
| `main` | repo root | `oj/oj<id>-<Name>[ ✅]/`, Learning Logs `oj<id>/`, `recommended/`, `README.md` |
| `OP` | `.op/` (gitignored on main) | `scripts/`, `data/`, `solutions/`, `docs/` |

`ijudge/paths.py` finds `main` through `git worktree list`; set
`PSCP_MAIN_ROOT` to point the scripts at another checkout (tests do this).

## Setup

```sh
git worktree add .op OP          # once, from the main checkout
pip install -r .op/scripts/requirements.txt
```

Commands that talk to iJudge need a session. Credentials come from the
environment only — nothing is hardcoded:

```sh
export IJUDGE_COOKIE='access_token=...'   # preferred: browser DevTools > Network > Cookie header, ~24h lifetime
# or let the scripts mint one:
export IJUDGE_USER=... IJUDGE_PASS=...
```

`submit_config.json` (gitignored) caches the session token. Never commit it.

## Commands

Everything goes through one entry point, run from the repo root:

```sh
python3 .op/scripts/pscp.py <command> [options]
```

| Command | Script | What it does | Network |
|---|---|---|---|
| `scrape` | `scrape_all_oj_problems.py` | iJudge → `data/*.json`, then renders the fetched problems. `--fast` = list + status only, `--only 3290-3301`, `--seed-code` | yes |
| `render` | `render_problems.py` | `data/` → problem folders on main: `problem.md`, `main.py` stub for new problems, ✅ sync. `--only`, `--check` | no |
| `status` | `sync_oj_status.py` | add/remove ` ✅` on `oj/` folders to match the registry | no |
| `test` | `run_samples.py` | run `main.py` against the official samples. `3290-3292`, `--week 9`, `--solutions` | no |
| `archive` | `archive_solutions.py` | copy solved `main.py` from main into `solutions/`. `--update`, `--restore IDS`, `--blank IDS` | no |
| `readme` | `update_readme.py` | regenerate `README.md` on main. `--check`, `--output PATH` | no |
| `doctor` | `check_repo.py` | consistency report: registry ↔ folders, ✅ vs status, archive drift, missing `submission.md` | no |
| `submit` | `submit_oj.py` | submit code from main to iJudge (interactive menu without arguments) | yes |

Every command that writes accepts `--dry-run`. `--dry-run` on `scrape` still
fetches; only writes are suppressed.

## Data

| File | Edited by | Holds |
|---|---|---|
| `data/course.json` | you | course ids, week windows by release date, week titles, `week_overrides`, category title tags, `folder_names`, `midterm_course_map` |
| `data/oj_problems.json` | `scrape` | summary registry: id, name, week, status, stats, deadline, `released`, category flags |
| `data/all_problems_detail.json` | `scrape` | statement, input/output spec, limits, sample cases, last submitted code |
| `data/course_84_problems.json` | you | the midterm problems of course 84 |
| `data/html_cache/` | `scrape` | raw pages for debugging the RSC parser (gitignored) |
| `solutions/oj<id>/main.py` | `archive` | finished reference code, keyed by id only |

### New teaching week

Add one entry to `weeks` in `course.json`:

```json
{"week": 14, "from": "2026-10-09", "title": "..."}
```

A week runs from its `from` date to the next entry's `from` (the last one for
7 days), in Bangkok time. A problem released outside every window keeps its
stored week and `doctor` warns about it. Mini Exams are put in week 14 by
`categories.mini_exam.week` — move that number first when a real week 14
arrives.

### Thai titles

New folders get an ASCII name from the title. A Thai title has none, so the
folder becomes bare `oj<id>`; add a name to `folder_names` and re-run
`render` before the folder is created, or rename it by hand.

## What the scripts may write

| File | Rule |
|---|---|
| `problem.md` | rewritten only if generated (marker comment or the legacy `## 1. โจทย์จริงจาก iJudge` heading) |
| `main.py` | created once; later only an untouched stub is refreshed (`ijudge.code.is_stub`) |
| `submission.md`, `ai_reflection.md`, `recommended/` | never |
| folder names | only the ` ✅` suffix, only under `oj/` |

## Layout

```
scripts/
  pscp.py                    single entry point
  ijudge/                    shared library — import, don't copy
    paths.py                 main / OP locations, problem folder index
    config.py                data/course.json: weeks, tags, folder names
    code.py                  main.py template, stub detection
    render.py                problem.md rendering, statement cleanup, ✅ sync
    course.py                raw iJudge record -> registry shape
    weeks.py                 week lookup, date formatting
    auth.py  client.py       iJudge session and HTTP
    fsio.py                  dry-run-aware writes, atomic JSON, safe renames
  tests/                     python3 -m unittest discover -s .op/scripts/tests -t .op/scripts
```

## ihelp

`ihelp/scripts/build_pscp_registry.py` and `verify_solutions.py` read
`.op/data/` and `.op/solutions/` directly (`PSCP_OP_ROOT` overrides the
location). Nothing here writes into ihelp.
