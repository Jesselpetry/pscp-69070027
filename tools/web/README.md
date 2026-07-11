# \<i\>help — PSCP Learning-Log Maker (Next.js)

Step-by-step `submission.md` / `ai_reflection.md` maker for IT KMITL PSCP
students, styled after [iJudge](https://ijudge.it.kmitl.ac.th).

The site never writes content for you: every wizard step only collects your
own words and formats them into the official course templates in
`AI-Guidelines-PSCP/templates/` (Thai or English). Nothing is submitted to
the OJ — you download the finished file and submit your code yourself.

## Run

Uses [Bun](https://bun.sh) as the package manager / script runner
(`bun.lock`), with Next.js executing on Node.

```bash
cd tools/web
bun install   # first time only
bun run dev   # http://localhost:3000
```

Note: do not force the Bun runtime with `bun --bun next ...` — Next 16's
build crashes under Bun 1.2.x (SIGTRAP). `bun run` as above is the supported
setup.

## Features

- **Master problem list** from `oj_problems.json` at the repo root
  (override with the `OJ_PROBLEMS_PATH` env var). Shows difficulty stars,
  class pass statistics, expire dates, and Learning Log tags straight from
  the export.
- **Week badges** derived from `expire_date`: the earliest distinct date =
  **Week 1**, the next = **Week 2**, and so on, with a week filter bar.
  Expired dates show in red.
- **Step-by-step md maker** — one wizard per file, one template section per
  step, with the official guidance text and collapsible *examples* excerpted
  from `AI-Guidelines-PSCP/examples/` (shown only to illustrate the expected
  level of detail).
- **Download to your machine** — preview the generated markdown, then
  download `submission.md` / `ai_reflection.md` and place it in your problem
  folder.
- **TH / EN toggle** — switches both the UI and which official template the
  file is generated from.
- **Drafts auto-saved** in the browser (localStorage), per problem.

## Notes

- The green/gray dot next to a problem name is the `status` recorded in
  `oj_problems.json`. Live status from iJudge is not fetched: iJudge's
  sign-in is a Next.js server-action flow, so there is no stable JSON API to
  integrate against — re-export `oj_problems.json` to refresh statuses.
- Learning logs are required only for problems tagged **Learning Log**;
  the maker still works for other problems if you want notes for yourself.
