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

Commands that talk to iJudge need an active session. The tools resolve this
automatically in the following order:

1. `IJUDGE_COOKIE` environment variable (if non-expired).
2. Cached token in `submit_config.json` (if non-expired).
3. **Auto-refresh from local browser profile** (e.g. Zen Browser SQLite cookies).
4. Automated sign-in via `IJUDGE_USER` and `IJUDGE_PASS`.

To set or override manually:
```sh
export IJUDGE_COOKIE='access_token=...'            # browser DevTools > Network > Cookie header, ~24h lifetime
python3 .op/scripts/pscp.py submit --set-cookie    # or paste & save it interactively
# or let the scripts mint one:
export IJUDGE_USER=... IJUDGE_PASS=...
```

`submit_config.json` (gitignored) caches the session token. Never commit it.

## Fast-Track Workflow

When new problems are dropped:

```sh
# 1. Scrape & create stubs
python3 .op/scripts/pscp.py scrape --only <ids>

# 2. Write code on main in oj/oj<id>-<Name>/main.py, then test
python3 .op/scripts/pscp.py test <id>

# 3. Submit directly to iJudge
python3 .op/scripts/pscp.py submit --ids <ids> --yes

# 4. Post-pass sync (status + archive + readme + doctor)
python3 .op/scripts/pscp.py status && python3 .op/scripts/pscp.py archive && python3 .op/scripts/pscp.py readme && python3 .op/scripts/pscp.py doctor

# 5. Commit & push both branches
git add -A && git commit -m "feat(oj): complete <ids>, update README" && git push origin main
git -C .op add -A && git -C .op commit -m "feat(solutions): add <ids> solutions" && git -C .op push origin OP
```

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
| `web` | `web_app.py` | local dashboard at http://127.0.0.1:8765: sign in, progress, submit to iJudge, run the commands above | yes |

Every command that writes accepts `--dry-run`. `--dry-run` on `scrape` still
fetches; only writes are suppressed.

## Web dashboard

```sh
python3 .op/scripts/pscp.py web                 # opens http://127.0.0.1:8765
python3 .op/scripts/pscp.py web --port 9000 --no-browser
```

1. **Sign in** with an iJudge access token (or cookie), or username + password. The password is used once to mint a token and never stored; the token goes to `submit_config.json`. A saved token that is still valid skips this page.
2. Right after signing in it runs `scrape --fast`, so the dashboard shows that account's current status.
3. **ภาพรวม** — passed / not passed, code on main vs stubs, "พร้อมส่ง" (code written, not passed yet), per-week and per-category progress, upcoming deadlines, Learning Logs without `submission.md`.
4. **โจทย์** — quick filters, search, week filter, row checkboxes. A row opens `problem.md` / `main.py` with "ทดสอบกับ sample" and "ส่งข้อนี้".
5. **ส่งเข้า iJudge** — choose the selected rows, a whole week, everything with code that has not passed, or everything; options skip passed problems and include Learning Logs. A preview lists what will be sent and why the rest is skipped (no main.py, stub, passed, Learning Log) plus lint warnings; after confirming, each problem shows its live verdict, score and PEP8. Submissions reuse `submit_oj.submit_problem` / `poll_submission_status`; stubs are never sent. Status is refreshed afterwards.
6. **เครื่องมือ** — one-button cards for every other command; extra options are folded under each card.

It binds to 127.0.0.1 only; POSTs need a per-launch token embedded in the page and the Host header must be this server, so other sites in the browser cannot drive it. Deep links: `#overview`, `#problems`, `#tools`.

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
  web_app.py, web/           local dashboard (stdlib http.server + one HTML page)
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
