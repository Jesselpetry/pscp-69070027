# scripts/

Automation for the PSCP course archive: scraping problems from iJudge,
submitting solutions, and regenerating the repo README.

## Setup

Credentials come from the environment. Copy `../.env.example` to `../.env` and
fill it in, or export the variables directly:

```sh
export IJUDGE_COOKIE='access_token=...'   # preferred, ~24h lifetime
# or, to mint a cookie automatically:
export IJUDGE_USER=... IJUDGE_PASS=...
```

Nothing is hardcoded and there are no defaults — a script that cannot find a
credential fails with an explanatory error rather than guessing.

## Commands

| Command | What it does |
|---|---|
| `python3 scrape_all_oj_problems.py` | Full scrape: HTML cache, detail JSON, `problem.md`, seeded `main.py` |
| `python3 scrape_all_oj_problems.py --fast` | Summary registry only — one request, no per-problem fetch |
| `python3 scrape_all_oj_problems.py --only 3290-3301` | Restrict the detail fetch to some ids |
| `python3 submit_oj.py --ids 3226,3237` | Submit solutions (interactive menu with no arguments) |
| `python3 sync_oj_status.py` | Rename `oj/` folders to match pass status |
| `python3 update_readme.py` | Regenerate the repo README from the registries |

Every script that writes to disk accepts `--dry-run`, which prints the planned
changes to stderr and touches nothing. Use it first when in doubt.

## Layout

```
scripts/
  ijudge/                    shared library — import, don't copy
    auth.py                  credentials, sign-in, cookie caching
    client.py                retrying HTTP, RSC stream helpers
    course.py                raw iJudge record -> registry shape
    fsio.py                  dry-run-aware writes, atomic JSON, safe renames
    weeks.py                 course-week classifier, date formatting
  scrape_all_oj_problems.py
  submit_oj.py
  sync_oj_status.py
  update_readme.py
```

`ijudge/` exists because `get_week`, `login`, `resolve_cookie` and
`format_expire_date` were previously copy-pasted across four scripts, so a new
teaching week meant editing all four consistently or the two repos silently
disagreed. Add shared behaviour there, not in a second copy.

## Where solutions live

One copy per problem, no exceptions:

| Kind | Home | Example |
|---|---|---|
| Normal problem | `oj/oj<id>-<Name>/main.py` | `oj/oj3290-Left_Arrow/main.py` |
| Learning Log | `oj<id>/main.py` (repo root) | `oj3293/main.py` |

The scraper writes `problem.md` and seeds `main.py` in these locations, and
`ihelp/scripts/build_pscp_registry.py` indexes them into the app. Never keep a
second copy elsewhere — a stale duplicate silently wins or loses depending on
which tool reads it first.

Verify solutions against their official samples with:

```sh
python3 ../../ihelp/scripts/verify_solutions.py          # all
python3 ../../ihelp/scripts/verify_solutions.py --week 9
```

## Notes

- `--dry-run` still performs every network fetch; only writes are suppressed.
  A full preview therefore takes as long as a real run.
- `submit_config.json` caches the session token. It is gitignored and holds a
  short-lived bearer token — do not commit it.
- The scraper writes the registries into **both** repos (`pscp-69070027/` and
  `../ihelp/`), which assumes the two are checked out as siblings. The raw
  `data/html_cache/` is written here only, and is gitignored.
