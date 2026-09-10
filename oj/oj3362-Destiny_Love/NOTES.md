# oj3362 — disputed official sample

`main.py` passes official sample 1 and matches the statement's own worked
example (`$www$w$`), but official sample 2 shows `$$www$w$` — an extra leading
`$` that the prose does not explain.

The solution follows the prose. Consequences:

- `scripts/verify_solutions.py` lists this problem as DISPUTED rather than
  failing the run (see `KNOWN_DISPUTED` there).
- `edgeCases` for 3362 are cleared in `ihelp/data/pscp/problems.json` so the
  in-app grader never asserts the disputed expected value.

If iJudge corrects the sample, drop the `KNOWN_DISPUTED` entry and re-run
`bun run pscp:build`.
