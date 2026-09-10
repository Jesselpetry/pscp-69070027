#!/usr/bin/env python3
"""Scrape PSCP OJ problems from iJudge into both repos.

Produces, for every problem in the course:
  * an HTML cache of the problem page (data/html_cache/)
  * a structured detail record (data/all_problems_detail.json)
  * a formatted problem.md in the problem's folder
  * main.py seeded from the user's saved iJudge code, when the local file is
    still an untouched stub

It resolves Next.js RSC binary byte streams and $xx string references, and
merges into the existing registries rather than replacing them, so problems
iJudge no longer lists keep their history.

Run:
    python3 scripts/scrape_all_oj_problems.py [--dry-run] [--fast] [--only IDS]

    --fast   refresh the summary registry only: one request for the course
             listing, no per-problem detail fetch. This replaces the old
             sync_oj_problems.py, which did exactly this and nothing else.
    --only   restrict the detail fetch to ids/ranges, e.g. --only 3226,3290-3301
"""

import argparse
import html
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ijudge import (  # noqa: E402
    AuthError,
    HttpError,
    build_problem_item,
    ensure_dir,
    fetch,
    fetch_problem_list,
    is_dry_run,
    rename_dir,
    resolve_cookie,
    safe_write_json,
    set_dry_run,
    summary_fields,
    write_text,
)

PSCP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IHELP_ROOT = os.path.normpath(os.path.join(PSCP_ROOT, "..", "ihelp"))

# Raw page cache: a scrape artifact for debugging the RSC parsers. Nothing in
# the ihelp app reads it, so it lives in the archive repo only (7.2MB) and is
# gitignored rather than being mirrored into both repos.
HTML_CACHE_DIR = os.path.join(PSCP_ROOT, "data", "html_cache")

JSON_OUT_PSCP = os.path.join(PSCP_ROOT, "data", "all_problems_detail.json")
JSON_OUT_IHELP = os.path.join(IHELP_ROOT, "data", "all_problems_detail.json")

OJ_PROBLEMS_PSCP = os.path.join(PSCP_ROOT, "oj_problems.json")
OJ_PROBLEMS_IHELP = os.path.join(IHELP_ROOT, "data", "oj_problems.json")

# Politeness delay between per-problem fetches against a university server.
FETCH_DELAY_SEC = 0.15

FOLDER_ALIASES = {
    3290: "Left_Arrow",
    3291: "Right_Arrow",
    3292: "Arrow",
    3294: "Teaching_schedule",
    3295: "Electric_Using",
    3297: "Movie_Ticket_Trouble",
    3298: "Little_Rabbit_Loves_BUU",
    3300: "Life_Balance",
    3301: "Put_In_Box",
    3349: "Bowl_Stack",
    3350: "Sell_Car",
    3351: "Rabbit_Language",
    3352: "LastStand",
    3353: "PickThemAgain",
    3354: "Hint",
    3356: "Bus_Seat",
    3358: "Pig",
    3359: "Bowl_Stack_II",
    3361: "Sell_Car_II",
    3362: "Destiny_Love",
    3363: "New_Rabbit_Flu_Strain",
}

STUB_MARKER = "# solution code here"


def clean_text(t):
    if not t:
        return ""
    if not isinstance(t, str):
        t = str(t)
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    return t.strip()


def stub_solution(problem_name):
    """Placeholder main.py body written when iJudge has no saved code."""
    return "\n".join([
        f'""" {problem_name} """',
        "",
        "",
        "def main():",
        f'    """{problem_name}"""',
        f"    {STUB_MARKER}",
        "",
        "",
        'if __name__ == "__main__":',
        "    main()",
        "",
    ])


def is_placeholder(code):
    """True if `code` is an untouched stub that is safe to overwrite.

    Deliberately conservative: a short but genuine solution must not be
    clobbered by the server's beforeCode. Only the marker comment counts, not
    line count -- plenty of real PSCP answers are one or two lines.
    """
    return STUB_MARKER in code or not code.strip()


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

def format_problem_markdown(data):
    cp = data.get("courseProblem", {})
    prob = data.get("problem", {})
    samples = data.get("sampleCases", [])
    
    cp_id = cp.get("cp_id", prob.get("problem_id", 0)) if cp else prob.get("problem_id", data.get("id", 0))
    title = cp.get("cp_title", prob.get("problem_title", data.get("name", f"OJ {cp_id}"))) if cp else data.get("name", f"OJ {cp_id}")
    timeout = cp.get("cp_timeout", 1) if cp else 1
    memory_limit = cp.get("cp_memory_limit", 32000) if cp else 32000
    note = prob.get("problem_note", "").strip() if prob else ""
    
    desc = clean_text(prob.get("problem_description", "")) if prob else ""
    input_spec = clean_text(prob.get("problem_input_specification", "")) if prob else ""
    output_spec = clean_text(prob.get("problem_output_specification", "")) if prob else ""
    
    md_lines = []
    md_lines.append(f"# OJ {cp_id}: {title}")
    md_lines.append("")
    md_lines.append(f"> - **iJudge cp_id**: {cp_id} — ภาษา Python")
    md_lines.append(f"> - **เวลาจำกัด**: {timeout} วินาที | **หน่วยความจำ**: {memory_limit:,} KB")
    if note:
        md_lines.append(f"> - **โน้ตจากผู้ออกโจทย์**: {note}")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 1. โจทย์จริงจาก iJudge")
    md_lines.append("")
    md_lines.append(desc if desc else "*(ไม่มีคำอธิบายเพิ่มเติม)*")
    md_lines.append("")
    md_lines.append("## 2. Input Specification")
    md_lines.append("")
    md_lines.append(input_spec if input_spec else "*(ไม่มีข้อกำหนดอินพุต)*")
    md_lines.append("")
    md_lines.append("## 3. Output Specification")
    md_lines.append("")
    md_lines.append(output_spec if output_spec else "*(ไม่มีข้อกำหนดเอาต์พุต)*")
    md_lines.append("")
    md_lines.append("## 4. ตัวอย่างจาก iJudge")
    md_lines.append("")
    
    if samples:
        for idx, s in enumerate(samples, 1):
            inp = clean_text(s.get("testcase_input", ""))
            out = clean_text(s.get("testcase_output", ""))
            md_lines.append(f"### ตัวอย่างที่ {idx}")
            md_lines.append("- **อินพุต**:")
            md_lines.append("  ```text")
            if inp:
                for line in inp.split("\n"):
                    md_lines.append(f"  {line}")
            else:
                md_lines.append("  (ไม่มีอินพุต)")
            md_lines.append("  ```")
            md_lines.append("- **เอาต์พุต**:")
            md_lines.append("  ```text")
            if out:
                for line in out.split("\n"):
                    md_lines.append(f"  {line}")
            else:
                md_lines.append("  (ไม่มีเอาต์พุต)")
            md_lines.append("  ```")
            md_lines.append("")
    else:
        md_lines.append("*(ไม่มีตัวอย่าง Sample Testcase)*")
        md_lines.append("")
        
    return "\n".join(md_lines).strip() + "\n"

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


def scrape_all(fast=False, only_ids=None, seed_code=False):
    for d in (HTML_CACHE_DIR,
              os.path.dirname(JSON_OUT_PSCP), os.path.dirname(JSON_OUT_IHELP)):
        ensure_dir(d)

    cookie = resolve_cookie()

    # Step 1: Load the existing registries FIRST, so historical flags (notably
    # [Recommend], which iJudge drops from the title once a deadline passes) are
    # available while the new records are being built rather than patched after.
    print("=== Step 1: Loading Existing Databases ===")
    existing_details_map = {}
    if os.path.exists(JSON_OUT_PSCP):
        try:
            with open(JSON_OUT_PSCP, "r", encoding="utf-8") as f:
                for rec in json.load(f):
                    existing_details_map[rec["id"]] = rec
            print(f"Loaded {len(existing_details_map)} existing detailed problems.")
        except (OSError, ValueError) as e:
            print(f"Warning: failed to load {JSON_OUT_PSCP}: {e}", file=sys.stderr)

    existing_oj_map = {}
    if os.path.exists(OJ_PROBLEMS_PSCP):
        try:
            with open(OJ_PROBLEMS_PSCP, "r", encoding="utf-8") as f:
                for rec in json.load(f):
                    existing_oj_map[rec["id"]] = rec
            print(f"Loaded {len(existing_oj_map)} existing summary records.")
        except (OSError, ValueError) as e:
            print(f"Warning: failed to load {OJ_PROBLEMS_PSCP}: {e}", file=sys.stderr)

    # Step 2: Fetch the live course listing.
    print("\n=== Step 2: Fetching Course 78 Problems List ===")
    raw_problems = fetch_problem_list(cookie, course_id=78)
    print(f"Found {len(raw_problems)} problems in Course 78.")

    parsed_course_items = [
        build_problem_item(raw, idx, existing_oj_map)
        for idx, raw in enumerate(raw_problems)
    ]

    if fast:
        print("--fast: skipping per-problem detail fetch.")
        detail_targets = []
    elif only_ids:
        detail_targets = [i for i in parsed_course_items if i["id"] in only_ids]
        print(f"--only: {len(detail_targets)} of {len(parsed_course_items)} problems selected.")
    else:
        detail_targets = list(parsed_course_items)

    # Step 3: Scrape details, HTML cache and RSC data for the selected problems.
    failures = []
    if detail_targets:
        print("\n=== Step 3: Scraping Problem Details & HTML Caches ===")
    for idx_item, item in enumerate(detail_targets, 1):
        pid = item["id"]
        p_name = item["name"]
        p_url = item["url"]
        is_ll = item["is_learning_log"]
        is_rec = item["is_recommended"]
        is_passed = item["status"] == "Passed"
        print(f"[{idx_item:2d}/{len(detail_targets)}] OJ {pid:4d}: {p_name} ...",
              end="", flush=True)

        try:
            rsc_text = fetch(p_url, cookie, rsc=True)
            html_text = fetch(p_url, cookie, rsc=False)
        except HttpError as e:
            print(f" [FAIL] {e}", file=sys.stderr)
            failures.append(pid)
            continue

        if html_text:
            write_text(os.path.join(HTML_CACHE_DIR, f"oj{pid}.html"), html_text)

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
        print(" done")

        problem_md_content = format_problem_markdown(prob_detail)

        # 1. Learning Logs live only at the repo root, as ojXXXX/
        if is_ll:
            ll_dir = os.path.join(PSCP_ROOT, f"oj{pid}")
            ensure_dir(ll_dir)
            write_text(os.path.join(ll_dir, "problem.md"), problem_md_content)
            main_py_ll = os.path.join(ll_dir, "main.py")
            if not os.path.exists(main_py_ll):
                write_text(main_py_ll, (before_code if seed_code else None) or stub_solution(p_name))
            elif before_code and seed_code:
                with open(main_py_ll, "r", encoding="utf-8", errors="ignore") as f:
                    if is_placeholder(f.read()):
                        write_text(main_py_ll, before_code)

        # 2. Recommended problems also get a copy under recommended/
        if is_rec:
            rec_root = os.path.join(PSCP_ROOT, "recommended")
            rec_folders = [
                d for d in os.listdir(rec_root)
                if f"oj{pid}-" in d or d == f"oj{pid}"
            ] if os.path.isdir(rec_root) else []
            if rec_folders:
                write_text(os.path.join(rec_root, rec_folders[0], "problem.md"),
                           problem_md_content)

        # 3. Everything that is not a Learning Log lives under oj/
        if not is_ll:
            oj_root = os.path.join(PSCP_ROOT, "oj")
            oj_folders = [
                d for d in os.listdir(oj_root)
                if f"oj{pid}-" in d or d == f"oj{pid}"
            ] if os.path.isdir(oj_root) else []

            if oj_folders:
                target_dir_name = oj_folders[0]
                clean_name = target_dir_name.replace(" ✅", "").strip()
                desired_name = f"{clean_name} ✅" if is_passed else clean_name
                if desired_name != target_dir_name:
                    renamed = rename_dir(os.path.join(oj_root, target_dir_name),
                                         os.path.join(oj_root, desired_name))
                    # Under --dry-run the rename did not actually happen, so keep
                    # reading and writing through the current name.
                    if renamed and not is_dry_run():
                        target_dir_name = desired_name

                oj_dir_target = os.path.join(oj_root, target_dir_name)
                write_text(os.path.join(oj_dir_target, "problem.md"), problem_md_content)
                main_py_target = os.path.join(oj_dir_target, "main.py")
                if os.path.exists(main_py_target) and before_code and seed_code:
                    with open(main_py_target, "r", encoding="utf-8", errors="ignore") as f:
                        if is_placeholder(f.read()):
                            write_text(main_py_target, before_code)
            else:
                alias = FOLDER_ALIASES.get(pid)
                if alias:
                    folder_name = f"oj{pid}-{alias}"
                else:
                    safe_name = re.sub(r"[^\w\s-]", "", p_name).strip().replace(" ", "_")
                    folder_name = f"oj{pid}-{safe_name}"
                if is_passed:
                    folder_name += " ✅"
                oj_dir_target = os.path.join(oj_root, folder_name)
                ensure_dir(oj_dir_target)
                write_text(os.path.join(oj_dir_target, "problem.md"), problem_md_content)
                write_text(os.path.join(oj_dir_target, "main.py"),
                           (before_code if seed_code else None) or stub_solution(p_name))

        time.sleep(FETCH_DELAY_SEC)

    # Step 4: Merge and save the master registries.
    print("\n=== Step 4: Merging & Saving Master Databases ===")
    for item in parsed_course_items:
        existing_oj_map[item["id"]] = summary_fields(item)

    all_sorted_problems = sorted(existing_oj_map.values(), key=lambda x: x["id"])
    all_sorted_details = sorted(existing_details_map.values(), key=lambda x: x["id"])

    safe_write_json(JSON_OUT_PSCP, all_sorted_details)
    safe_write_json(JSON_OUT_IHELP, all_sorted_details)
    print(f"Saved detailed database ({len(all_sorted_details)} problems).")

    safe_write_json(OJ_PROBLEMS_PSCP, all_sorted_problems)
    safe_write_json(OJ_PROBLEMS_IHELP, all_sorted_problems)
    print(f"Saved summary database ({len(all_sorted_problems)} problems).")

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


def parse_id_selection(raw):
    """Parse '3226,3290-3301' into a set of problem ids."""
    ids = set()
    for token in raw.split(","):
        token = token.strip()
        if not token:
            continue
        if "-" in token:
            start, end = token.split("-", 1)
            ids.update(range(int(start), int(end) + 1))
        else:
            ids.add(int(token))
    return ids


def main():
    parser = argparse.ArgumentParser(
        description="Scrape all PSCP OJ problems from iJudge into both repos.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview directory renames and file modifications without executing changes.",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Refresh the summary registry only (one request, no per-problem detail fetch).",
    )
    parser.add_argument(
        "--only",
        metavar="IDS",
        help="Limit the detail fetch to these ids/ranges, e.g. 3226,3290-3301.",
    )
    parser.add_argument(
        "--seed-code",
        action="store_true",
        help=(
            "Seed empty main.py stubs with the code saved on iJudge. Off by "
            "default: the working branch deliberately keeps empty stubs, and "
            "the finished solutions live on the solutions/* branch."
        ),
    )
    args = parser.parse_args()

    set_dry_run(args.dry_run)
    if args.dry_run:
        print("[DRY-RUN] No files will be written. Network fetches still happen.",
              file=sys.stderr)

    try:
        only_ids = parse_id_selection(args.only) if args.only else None
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
