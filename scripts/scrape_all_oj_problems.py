#!/usr/bin/env python3
"""Scrape PSCP OJ problems from iJudge into the OP registries, then render.

Writes, on the OP branch:
  * data/oj_problems.json          summary registry (every listed problem)
  * data/all_problems_detail.json  detail records: statement, samples,
                                   limits, beforeCode
  * data/html_cache/oj<id>.html    raw page cache for debugging (gitignored)

Both registries are merged into rather than replaced, so problems iJudge no
longer lists keep their history. Problem pages are Next.js RSC streams; the
parsers below resolve their binary `T` chunks and `$xx` string references.

After the registries are saved, the fetched problems are rendered onto main
by the same code as render_problems.py (folder, ✅ status, problem.md, main.py
stub). ihelp reads the registries from OP directly; nothing is mirrored.

Run (from the repo root):
    python3 .op/scripts/scrape_all_oj_problems.py [--dry-run] [--fast]
                                                  [--only IDS] [--seed-code]

    --fast       refresh the summary registry only: one request for the course
                 listing, no per-problem detail fetch and no rendering
    --only       restrict the detail fetch (and rendering) to ids/ranges,
                 e.g. --only 3226,3290-3301
    --seed-code  replace an untouched main.py stub with the code saved on
                 iJudge (beforeCode); never touches a file with real code

Exit codes: 0 ok, 1 some problems failed to fetch, 2 auth, 3 HTTP, 130 ^C.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ijudge import (  # noqa: E402
    AuthError,
    HttpError,
    build_problem_item,
    config,
    ensure_dir,
    fetch,
    fetch_problem_list,
    paths,
    resolve_cookie,
    safe_write_json,
    set_dry_run,
    summary_fields,
    write_text,
)
from ijudge import render  # noqa: E402

# Politeness delay between per-problem fetches against a university server.
FETCH_DELAY_SEC = 0.15


def parse_rsc_stream(text):
    raw_bytes = text.encode("utf-8")
    pos = 0
    chunks = {}

    while pos < len(raw_bytes):
        colon_idx = raw_bytes.find(b":", pos)
        if colon_idx == -1:
            break
        chunk_id = raw_bytes[pos:colon_idx].decode("utf-8", errors="ignore").strip()

        after = raw_bytes[colon_idx+1 : colon_idx+3]
        if after.startswith(b"T"):
            comma_idx = raw_bytes.find(b",", colon_idx)
            if comma_idx == -1:
                break
            hex_len = raw_bytes[colon_idx+2 : comma_idx].decode("utf-8", errors="ignore")
            try:
                byte_len = int(hex_len, 16)
                body = raw_bytes[comma_idx+1 : comma_idx+1+byte_len].decode("utf-8", errors="ignore")
                chunks[chunk_id] = body
                pos = comma_idx + 1 + byte_len
                if pos < len(raw_bytes) and raw_bytes[pos:pos+1] == b"\n":
                    pos += 1
            except Exception:
                pos = comma_idx + 1
        else:
            next_nl = raw_bytes.find(b"\n", colon_idx)
            if next_nl == -1:
                body = raw_bytes[colon_idx+1:].decode("utf-8", errors="ignore")
                pos = len(raw_bytes)
            else:
                body = raw_bytes[colon_idx+1 : next_nl].decode("utf-8", errors="ignore")
                pos = next_nl + 1
            chunks[chunk_id] = body

    return chunks


def resolve_rsc_ref(val, chunks):
    if isinstance(val, str) and val.startswith("$") and len(val) <= 6 and val[1:].isalnum():
        ref_id = val[1:]
        if ref_id in chunks:
            raw = chunks[ref_id]
            if raw.startswith('"') and raw.endswith('"'):
                try:
                    return json.loads(raw)
                except Exception:
                    return raw[1:-1]
            return raw
    return val


def parse_balanced_json(s, key, start_char, end_char):
    target = f'"{key}":'
    pos = s.find(target)
    if pos == -1:
        return None
    start = s.find(start_char, pos)
    if start == -1:
        return None
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(s)):
        c = s[i]
        if esc:
            esc = False
            continue
        if c == '\\':
            esc = True
            continue
        if c == '"':
            in_str = not in_str
            continue
        if not in_str:
            if c == start_char:
                depth += 1
            elif c == end_char:
                depth -= 1
                if depth == 0:
                    substr = s[start:i+1]
                    try:
                        return json.loads(substr)
                    except Exception:
                        return None
    return None


def extract_string_value(s, key):
    target = f'"{key}":'
    pos = s.find(target)
    if pos == -1:
        return None
    start = s.find('"', pos + len(target))
    if start == -1:
        return None
    esc = False
    for i in range(start + 1, len(s)):
        c = s[i]
        if esc:
            esc = False
            continue
        if c == '\\':
            esc = True
            continue
        if c == '"':
            substr = s[start:i+1]
            try:
                return json.loads(substr)
            except Exception:
                return s[start+1:i]
    return None


def _load_existing(path: str, label: str) -> dict[int, dict[str, Any]]:
    """A registry as {id: record}; a damaged file warns and counts as empty."""
    try:
        records = render.load_registry(path)
    except (OSError, ValueError, KeyError) as e:
        print(f"Warning: failed to load {path}: {e}", file=sys.stderr)
        return {}
    if records:
        print(f"Loaded {len(records)} existing {label}.")
    return records


def scrape_all(
    fast: bool = False,
    only_ids: set[int] | None = None,
    seed_code: bool = False,
) -> int:
    """Scrape, save the registries, render what was fetched. Returns #failures."""
    ensure_dir(paths.HTML_CACHE_DIR)

    cookie = resolve_cookie()

    # Step 1: Load the existing registries FIRST, so historical flags (notably
    # [Recommend], which iJudge drops from the title once a deadline passes) are
    # available while the new records are being built rather than patched after.
    print("=== Step 1: Loading Existing Databases ===")
    existing_details_map = _load_existing(paths.DETAIL_JSON, "detailed problems")
    existing_oj_map = _load_existing(paths.SUMMARY_JSON, "summary records")

    # Step 2: Fetch the live course listing.
    course = config.course_id()
    print(f"\n=== Step 2: Fetching Course {course} Problems List ===")
    raw_problems = fetch_problem_list(cookie, course_id=course)
    print(f"Found {len(raw_problems)} problems in Course {course}.")

    parsed_course_items = [
        build_problem_item(raw, idx, existing_oj_map, existing_details_map)
        for idx, raw in enumerate(raw_problems)
    ]

    if fast:
        print("--fast: skipping per-problem detail fetch and rendering.")
        detail_targets = []
    elif only_ids:
        detail_targets = [i for i in parsed_course_items if i["id"] in only_ids]
        print(f"--only: {len(detail_targets)} of {len(parsed_course_items)} problems selected.")
    else:
        detail_targets = list(parsed_course_items)

    # Step 3: Scrape details, HTML cache and RSC data for the selected problems.
    failures: list[int] = []
    fetched: list[int] = []
    if detail_targets:
        print("\n=== Step 3: Scraping Problem Details & HTML Caches ===")
    for idx_item, item in enumerate(detail_targets, 1):
        pid = item["id"]
        print(f"[{idx_item:2d}/{len(detail_targets)}] OJ {pid:4d}: {item['name']} ...",
              end="", flush=True)

        try:
            rsc_text = fetch(item["url"], cookie, rsc=True)
            html_text = fetch(item["url"], cookie, rsc=False)
        except HttpError as e:
            print(f" [FAIL] {e}", file=sys.stderr)
            failures.append(pid)
            continue

        if html_text:
            write_text(os.path.join(paths.HTML_CACHE_DIR, f"oj{pid}.html"), html_text)

        chunks = parse_rsc_stream(rsc_text) if rsc_text else {}
        full_combined = " ".join(chunks.values())

        prob_obj = parse_balanced_json(full_combined, "problem", "{", "}") if full_combined else None
        cp_obj = parse_balanced_json(full_combined, "courseProblem", "{", "}") if full_combined else None
        samples = parse_balanced_json(full_combined, "sampleCases", "[", "]") if full_combined else []
        submission = parse_balanced_json(full_combined, "submission", "{", "}") if full_combined else None
        before_code = extract_string_value(full_combined, "beforeCode") if full_combined else None

        if prob_obj:
            for k in ("problem_description", "problem_input_specification",
                      "problem_output_specification", "problem_note", "problem_title"):
                if k in prob_obj and isinstance(prob_obj[k], str):
                    prob_obj[k] = resolve_rsc_ref(prob_obj[k], chunks)

        if before_code and isinstance(before_code, str):
            before_code = resolve_rsc_ref(before_code, chunks)
            if before_code in ("$undefined", "$null") or (
                isinstance(before_code, str) and before_code.startswith("$")
            ):
                before_code = None

        prob_detail = dict(item)
        prob_detail.update({
            "courseProblem": cp_obj,
            "problem": prob_obj,
            "sampleCases": samples,
            "submission": submission,
            "beforeCode": before_code,
        })
        existing_details_map[pid] = prob_detail
        fetched.append(pid)
        print(" done")

        time.sleep(FETCH_DELAY_SEC)

    # Step 4: Merge and save the master registries.
    print("\n=== Step 4: Merging & Saving Master Databases ===")
    for item in parsed_course_items:
        existing_oj_map[item["id"]] = summary_fields(item)

    all_sorted_problems = sorted(existing_oj_map.values(), key=lambda x: x["id"])
    all_sorted_details = sorted(existing_details_map.values(), key=lambda x: x["id"])

    safe_write_json(paths.DETAIL_JSON, all_sorted_details)
    print(f"Saved detailed database ({len(all_sorted_details)} problems).")

    safe_write_json(paths.SUMMARY_JSON, all_sorted_problems)
    print(f"Saved summary database ({len(all_sorted_problems)} problems).")

    # Step 5: Render the fetched problems onto main. The in-memory registries
    # are passed so a --dry-run previews exactly what was just fetched.
    if fetched:
        print(f"\n=== Step 5: Rendering {len(fetched)} Problem Folders ===")
        stats = render.render_ids(
            fetched,
            seed_code=seed_code,
            summaries=existing_oj_map,
            details=existing_details_map,
        )
        print(stats.report())

    if failures:
        print(
            f"\n[!] {len(failures)} problem(s) failed to fetch and kept their "
            f"previous data: {', '.join(str(f) for f in failures)}",
            file=sys.stderr,
        )
        print("Scraping finished with errors.")
    else:
        print("\nScraping & synchronization finished successfully.")
    return len(failures)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scrape PSCP OJ problems from iJudge into the OP registries, "
                    "then render the fetched problems onto main.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch as usual but write nothing; planned writes go to stderr.",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Refresh the summary registry only (one request, no per-problem "
             "detail fetch, no rendering).",
    )
    parser.add_argument(
        "--only",
        metavar="IDS",
        help="Limit the detail fetch and rendering to these ids/ranges, "
             "e.g. 3226,3290-3301.",
    )
    parser.add_argument(
        "--seed-code",
        action="store_true",
        help=(
            "Replace untouched main.py stubs with the code saved on iJudge. Off "
            "by default: main deliberately keeps empty stubs, and the archived "
            "solutions live on OP under solutions/."
        ),
    )
    args = parser.parse_args()

    set_dry_run(args.dry_run)
    if args.dry_run:
        print("[DRY-RUN] No files will be written. Network fetches still happen.",
              file=sys.stderr)

    try:
        only_ids = render.parse_ids(args.only) if args.only else None
    except ValueError:
        parser.error(f"--only could not be parsed: {args.only!r}")

    try:
        return 1 if scrape_all(
            fast=args.fast, only_ids=only_ids, seed_code=args.seed_code
        ) else 0
    except AuthError as e:
        print(f"[!] {e}", file=sys.stderr)
        return 2
    except HttpError as e:
        print(f"[!] iJudge request failed: {e}", file=sys.stderr)
        return 3
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
