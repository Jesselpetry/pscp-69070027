#!/usr/bin/env python3
"""
Standardized CLI tool to submit PSCP OJ problems to iJudge.

Features:
- Multi-Course Support: Regular PSCP (Course 78) & Midterm Exam (Course 84).
- Configurable targeting: by Expire Date, Week, Specific Problem IDs, Range, or All.
- Interactive Cookie Management: Enter, update, validate, and persist iJudge session cookies.
- Auto-filters out Learning Logs by default.
- Pre-submission lint checks (pylint warnings & sys.stdin.read detection).
- Beautiful terminal preview table with explicit confirmation prompt.
- Real-time submission progress and live score/PEP8 polling.
"""

import argparse
import glob
import json
import os
import random
import re
import sys
import time
import urllib.request
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ijudge import USER_AGENT, load_config, save_config, validate_cookie  # noqa: E402

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PSCP_ROOT = os.path.dirname(SCRIPT_DIR)
WORKSPACE_ROOT = os.path.dirname(PSCP_ROOT)
CONFIG_FILE = os.path.join(PSCP_ROOT, "submit_config.json")
PROBLEMS_JSON = os.path.join(PSCP_ROOT, "oj_problems.json")
COURSE_84_JSON = os.path.join(PSCP_ROOT, "data", "course_84_problems.json")
OJ_DIR = os.path.join(PSCP_ROOT, "oj")

DEFAULT_COURSE_ID = 78
CURRENT_ACTION_ID = "7fb7acaef042f69199bda46c6a7a0f2b05848f3aee"
DEFAULT_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/x-component",
    "Content-Type": "text/plain;charset=UTF-8",
    "next-action": CURRENT_ACTION_ID,
    "Origin": "https://ijudge.it.kmitl.ac.th"
}

# Alias map for Midterm Course 84 problem IDs to local directory keywords
MIDTERM_ALIAS_MAP = {
    3243: ["Stats"],
    3242: ["ijudge-itkmitl", "ijudge"],
    3143: ["Pizza_Time", "Pizza"],
    3138: ["ThaiPlus", "FakeThaiPlus"],
    3142: ["Triangle"],
    3146: ["Units"],
    3240: ["PM_Watch", "PM"],
    3239: ["Code_Cleaner", "Cleaner"],
    3148: ["RealThaiPlus", "RealThai"]
}


def find_cookie(cli_cookie=None, cli_cookie_file=None, config=None):
    """Resolve iJudge session cookie from various potential sources."""
    if cli_cookie and cli_cookie.strip():
        return cli_cookie.strip()

    if cli_cookie_file and os.path.exists(cli_cookie_file):
        try:
            with open(cli_cookie_file, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception:
            pass

    env_cookie = os.environ.get("IJUDGE_COOKIE")
    if env_cookie and env_cookie.strip():
        return env_cookie.strip()

    if config and config.get("cookie", "").strip():
        return config["cookie"].strip()

    for candidate in [
        os.path.join(PSCP_ROOT, ".ijudge_cookie"),
        os.path.join(WORKSPACE_ROOT, ".ijudge_cookie")
    ]:
        if os.path.exists(candidate):
            try:
                with open(candidate, "r", encoding="utf-8") as f:
                    c = f.read().strip()
                    if c:
                        return c
            except Exception:
                pass

    for env_file in [
        os.path.join(WORKSPACE_ROOT, ".env.local"),
        os.path.join(WORKSPACE_ROOT, ".env"),
        os.path.join(PSCP_ROOT, ".env.local"),
        os.path.join(PSCP_ROOT, ".env")
    ]:
        if os.path.exists(env_file):
            try:
                with open(env_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("IJUDGE_COOKIE="):
                            return line.split("=", 1)[1].strip().strip("\"'")
            except Exception:
                pass

    return None


def prompt_enter_cookie(config):
    """Prompt user to enter/update cookie interactively, validate it, and persist."""
    print("\n" + "=" * 65)
    print("  Enter iJudge Session Cookie")
    print("=" * 65)
    print("Paste your full iJudge Cookie string from your browser.")
    print("(e.g. from Browser DevTools > Network tab > Cookie header)")
    print("-" * 65)
    raw_input_cookie = input("Cookie: ").strip()
    if not raw_input_cookie:
        print("[!] No cookie entered. Operation cancelled.")
        return config.get("cookie", "")

    print("[*] Validating cookie with iJudge server...", end="", flush=True)
    auth_info = validate_cookie(raw_input_cookie)
    if auth_info["valid"]:
        print(f" ✅ Success!\n    Logged in as: {auth_info['username']} ({auth_info['fullname']})")
        config["cookie"] = raw_input_cookie
        save_config(config)
        return raw_input_cookie
    else:
        print(f" ❌ Validation Warning: {auth_info['error']}")
        save_anyway = input("Save this cookie anyway? [y/N]: ").strip().lower()
        if save_anyway in ("y", "yes"):
            config["cookie"] = raw_input_cookie
            save_config(config)
            return raw_input_cookie
        return config.get("cookie", "")


def load_all_problems(course_id=DEFAULT_COURSE_ID):
    """Load problems from appropriate JSON registry depending on course ID."""
    if course_id == 84:
        if os.path.exists(COURSE_84_JSON):
            with open(COURSE_84_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    if not os.path.exists(PROBLEMS_JSON):
        print(f"[!] Error: {PROBLEMS_JSON} not found.")
        sys.exit(1)
    with open(PROBLEMS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def find_solution_file(problem_id, problem_name=""):
    """Locate the Python solution file for a problem."""
    # 1. Direct ID matching in oj/oj<id>-*
    for path in glob.glob(os.path.join(OJ_DIR, f"oj{problem_id}-*")):
        if os.path.isdir(path):
            main_py = os.path.join(path, "main.py")
            if os.path.exists(main_py):
                return main_py

    # 2. Check root-level oj<id> directories
    root_oj = os.path.join(PSCP_ROOT, f"oj{problem_id}")
    if os.path.isdir(root_oj):
        main_py = os.path.join(root_oj, "main.py")
        if os.path.exists(main_py):
            return main_py

    # 3. Check Midterm Alias Map (for Course 84)
    if problem_id in MIDTERM_ALIAS_MAP:
        for keyword in MIDTERM_ALIAS_MAP[problem_id]:
            for p in glob.glob(os.path.join(OJ_DIR, f"*{keyword}*")):
                main_py = os.path.join(p, "main.py")
                if os.path.exists(main_py):
                    return main_py

    # 4. Check problem name in oj directory
    if problem_name:
        sanitized = re.sub(r"[^\w\s]", "", problem_name).strip().replace(" ", "_")
        for p in glob.glob(os.path.join(OJ_DIR, f"*{sanitized}*")):
            main_py = os.path.join(p, "main.py")
            if os.path.exists(main_py):
                return main_py

    # 5. Check loose files across repo
    candidates = glob.glob(os.path.join(PSCP_ROOT, "**", f"*{problem_id}*.py"), recursive=True)
    candidates = [c for c in candidates if not c.endswith("problem.md") and not "scripts" in c and not "node_modules" in c]
    if candidates:
        return candidates[0]

    return None


def lint_check_code(code):
    """Perform quick safety checks on Python code prior to submission."""
    warnings = []
    if "sys.stdin.read()" in code:
        warnings.append("uses 'sys.stdin.read()' (Grader Runtime Error risk)")
    if "day == 0" in code:
        warnings.append("uses 'day == 0' (PEP8 simplification warning)")
    if "range(len(" in code:
        warnings.append("uses 'range(len(...))' (Consider using enumerate)")
    return warnings


def filter_problems(all_problems, args, config):
    """Filter problems based on CLI arguments or interactive choices."""
    exclude_ll = not args.include_learning_log if hasattr(args, "include_learning_log") else config.get("exclude_learning_logs", True)

    filtered = []
    # args.course_id is None unless --course-id was passed; fall back to the
    # configured course so an --ids/--week run does not report "Course None"
    # and post to an unset course.
    resolved_course = args.course_id or config.get("course_id", DEFAULT_COURSE_ID)

    if args.ids:
        target_ids = set()
        for token in args.ids.split(","):
            token = token.strip()
            if "-" in token:
                start, end = map(int, token.split("-", 1))
                target_ids.update(range(start, end + 1))
            elif token.isdigit():
                target_ids.add(int(token))
        filtered = [p for p in all_problems if p.get("id") in target_ids]

    elif args.expire:
        query = args.expire.strip().lower()
        filtered = [p for p in all_problems if query in p.get("expire_date", "").lower()]

    elif args.week is not None:
        target_weeks = set()
        for token in str(args.week).split(","):
            if token.strip().isdigit():
                target_weeks.add(int(token.strip()))
        filtered = [p for p in all_problems if p.get("week") in target_weeks]

    elif args.all or args.midterm:
        filtered = list(all_problems)
        if args.midterm:
            resolved_course = 84

    else:
        filtered, chosen_course = interactive_selection_menu(all_problems, config)
        if chosen_course:
            resolved_course = chosen_course

    if exclude_ll:
        filtered = [p for p in filtered if not p.get("is_learning_log", False) and "Learning Log" not in p.get("name", "")]

    if getattr(args, "recommended_only", False):
        filtered = [p for p in filtered if p.get("is_recommended", False)]

    filtered.sort(key=lambda p: p.get("id", 0))
    return filtered, resolved_course


def interactive_selection_menu(all_problems, config):
    """Render interactive CLI menu to pick problem batch, course, or configure cookie."""
    while True:
        current_cookie = config.get("cookie", "")
        auth_status = "Checking..."
        if current_cookie:
            auth_info = validate_cookie(current_cookie)
            if auth_info["valid"]:
                auth_status = f"✅ Logged in as {auth_info['username']} ({auth_info['fullname']})"
            else:
                auth_status = "⚠️ Cookie Expired or Invalid"
        else:
            auth_status = "❌ No Cookie Set"

        print("\n" + "=" * 70)
        print("  PSCP iJudge Submission Tool")
        print(f"  Status: {auth_status}")
        print("=" * 70)

        expire_groups = {}
        for p in all_problems:
            exp = p.get("expire_date") or "No Expire Date"
            expire_groups.setdefault(exp, []).append(p)

        sorted_dates = sorted(expire_groups.keys(), key=lambda d: ("1" if "2026" in d else "2", d))

        print("Regular Course (Course 78) - Options:")
        for idx, d in enumerate(sorted_dates, 1):
            count = len(expire_groups[d])
            ll_count = sum(1 for p in expire_groups[d] if p.get("is_learning_log"))
            print(f"  [{idx:2d}] Expire: {d:<26} ({count} problems, {ll_count} Learning Logs)")
        
        print("\nSpecial Options:")
        print(f"  [ M] Midterm Exam (Course 84: 9 problems)")
        print(f"  [ W] Filter by Week (e.g. Week 1, 2, 3)")
        print(f"  [ I] Enter Specific Problem IDs / Ranges (e.g. 3155-3167, 3129)")
        print(f"  [ A] All Problems (Course 78, {len(all_problems)} total)")
        print(f"  [ C] Enter / Update iJudge Cookie")
        print(f"  [ Q] Quit")
        print("-" * 70)

        choice = input("Enter your choice: ").strip()
        if not choice or choice.lower() == "q":
            print("Aborted.")
            sys.exit(0)

        if choice.lower() == "c":
            prompt_enter_cookie(config)
            continue

        if choice.lower() == "m":
            m_probs = load_all_problems(course_id=84)
            return m_probs, 84

        if choice.isdigit() and 1 <= int(choice) <= len(sorted_dates):
            selected_date = sorted_dates[int(choice) - 1]
            return expire_groups[selected_date], 78
        elif choice.lower() == "w":
            weeks_str = input("Enter week numbers separated by comma (e.g. 1, 2, 5): ").strip()
            weeks = {int(w.strip()) for w in weeks_str.split(",") if w.strip().isdigit()}
            return [p for p in all_problems if p.get("week") in weeks], 78
        elif choice.lower() == "i":
            ids_str = input("Enter problem IDs or ranges (e.g. 3129, 3155-3167): ").strip()
            target_ids = set()
            for token in ids_str.split(","):
                token = token.strip()
                if "-" in token:
                    start, end = map(int, token.split("-", 1))
                    target_ids.update(range(start, end + 1))
                elif token.isdigit():
                    target_ids.add(int(token))
            return [p for p in all_problems if p.get("id") in target_ids], 78
        elif choice.lower() == "a":
            return list(all_problems), 78
        else:
            print("[!] Invalid choice. Please try again.")


def resolve_server_action_id(problem_id, cookie):
    """Fetch problem page and dynamically extract latest submitCodeToServer action ID."""
    global CURRENT_ACTION_ID
    try:
        url = f"https://ijudge.it.kmitl.ac.th/problems/{problem_id}/description?problemPage=0"
        headers = {"User-Agent": USER_AGENT, "Cookie": cookie}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            page_html = resp.read().decode("utf-8", errors="ignore")

        chunks = re.findall(r'\"static/chunks/([^\"]+)\"', page_html)
        for c in chunks:
            c_clean = c.replace("\\", "").strip()
            if "rightpanel" in c_clean or "default-" in c_clean:
                chunk_url = f"https://ijudge.it.kmitl.ac.th/_next/static/chunks/{c_clean}"
                creq = urllib.request.Request(chunk_url, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(creq, timeout=10) as cresp:
                    js = cresp.read().decode("utf-8", errors="ignore")
                    m = re.search(r'createServerReference\)\(\"([a-f0-9]+)\",[^,]+,[^,]+,[^,]+,\"submitCodeToServer\"', js)
                    if m:
                        CURRENT_ACTION_ID = m.group(1)
                        DEFAULT_HEADERS["next-action"] = CURRENT_ACTION_ID
                        return CURRENT_ACTION_ID
    except Exception:
        pass
    return CURRENT_ACTION_ID


def submit_problem(problem_id, code, cookie, course_id=DEFAULT_COURSE_ID, retry_action=True):
    """Submit a single problem to iJudge."""
    url = f"https://ijudge.it.kmitl.ac.th/problems/{problem_id}/description?problemPage=0"
    
    clean_code = code.rstrip() + "\n"
    
    payload = json.dumps([{
        "code": clean_code,
        "lang_type": "Python",
        "course_problem_id": problem_id,
        "course_id": course_id
    }]).encode("utf-8")

    headers = dict(DEFAULT_HEADERS)
    headers["next-action"] = CURRENT_ACTION_ID
    headers["Cookie"] = cookie
    headers["Referer"] = url

    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 404 and retry_action:
            new_id = resolve_server_action_id(problem_id, cookie)
            if new_id and new_id != headers["next-action"]:
                return submit_problem(problem_id, code, cookie, course_id=course_id, retry_action=False)
        raise

    m_sub = re.search(r"\"submissionId\":\s*(\d+)", body)
    if m_sub:
        return int(m_sub.group(1))
    return None


def poll_submission_status(submission_id, cookie, poll_timeout=20.0, poll_interval=2.0):
    """Poll iJudge overview endpoint to retrieve submission result and PEP8 score."""
    url = f"https://ijudge.it.kmitl.ac.th/submissions/{submission_id}/overview"
    headers = {
        "User-Agent": DEFAULT_HEADERS["User-Agent"],
        "Accept": "*/*",
        "rsc": "1",
        "Cookie": cookie
    }

    start_time = time.time()
    last_info = {"result": "Pending", "score": 0.0, "pep8": 0.0, "ready": False}

    while time.time() - start_time < poll_timeout:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = resp.read().decode("utf-8")

            m_res = re.search(r"\"result\":\"([^\"]+)\"", body)
            m_score = re.search(r"\"score\":([\d\.]+)", body)
            m_pep8 = re.search(r"\"pep8_score\":([\d\.]+)", body)

            if m_res:
                result = m_res.group(1)
                score = float(m_score.group(1)) if m_score else 0.0
                pep8 = float(m_pep8.group(1)) if m_pep8 else 0.0
                last_info = {"result": result, "score": score, "pep8": pep8, "ready": False}

                if result not in ("Judging", "Pending", "In queue", "In Queue", "null", ""):
                    last_info["ready"] = True
                    return last_info
        except Exception:
            pass
        time.sleep(poll_interval)

    return last_info


def parse_delay_val(v, default_unit=None):
    if v is None:
        return None
    v = str(v).strip().lower()
    m = re.match(r"^([\d\.]+)\s*([a-z]*)$", v)
    if not m:
        return None
    val, unit = float(m.group(1)), m.group(2)
    unit = unit or default_unit
    if unit in ("m", "min", "mins", "minute", "minutes"):
        return val * 60.0
    elif unit in ("s", "sec", "secs", "second", "seconds"):
        return val
    elif unit in ("h", "hr", "hrs", "hour", "hours"):
        return val * 3600.0
    elif val <= 15:
        return val * 60.0
    else:
        return val


def parse_delay_range_str(s):
    if not s:
        return None, None
    s = s.strip().lower()
    m = re.match(r"^([\d\.]+)\s*(?:-|to)\s*([\d\.]+)\s*([a-z]*)$", s)
    if not m:
        return None, None
    low, high, unit = float(m.group(1)), float(m.group(2)), m.group(3)
    unit = unit if unit else ("m" if high <= 15 else "s")
    return parse_delay_val(f"{low}{unit}"), parse_delay_val(f"{high}{unit}")


def format_time_delta(total_seconds):
    """Format seconds into readable string (e.g. '4m 30s' or '1h 12m 45s')."""
    total_seconds = max(0, int(total_seconds))
    hrs, rem = divmod(total_seconds, 3600)
    mins, secs = divmod(rem, 60)
    if hrs > 0:
        return f"{hrs}h {mins:02d}m {secs:02d}s"
    elif mins > 0:
        return f"{mins}m {secs:02d}s"
    return f"{secs}s"


def run_countdown(seconds, next_problem_desc, remaining_batch_sec, est_finish_str):
    """Run an interactive countdown timer with estimated finish time."""
    end_time = time.time() + seconds
    try:
        while True:
            rem = end_time - time.time()
            if rem <= 0:
                break
            rem_sec = int(rem)
            rem_m, rem_s = divmod(rem_sec, 60)

            cur_batch_rem = max(0, int(remaining_batch_sec - (seconds - rem)))
            batch_str = format_time_delta(cur_batch_rem)

            status_line = (
                f"⏳ [Wait: {rem_m:02d}:{rem_s:02d}] "
                f"[Batch left: ~{batch_str}] "
                f"[Est. finish: {est_finish_str}] -> Next: {next_problem_desc}"
            )

            if sys.stdout.isatty():
                sys.stdout.write(f"\r\033[K{status_line}")
                sys.stdout.flush()
                time.sleep(1.0)
            else:
                if rem_sec % 30 == 0 or rem_sec == int(seconds):
                    sys.stdout.write(f"{status_line}\n")
                    sys.stdout.flush()
                time.sleep(1.0)

        if sys.stdout.isatty():
            sys.stdout.write("\r\033[K")
            sys.stdout.flush()
        return True
    except KeyboardInterrupt:
        if sys.stdout.isatty():
            sys.stdout.write("\n")
            print(f"\n[!] Countdown interrupted for {next_problem_desc}.")
            ans = input("Options: [S]kip wait and submit now | [Q]uit batch [S/q]: ").strip().lower()
            if ans == "q":
                return False
            print("[*] Skipping wait, proceeding to submit...")
            return True
        else:
            raise


def main():
    parser = argparse.ArgumentParser(description="Submit PSCP OJ problems to iJudge with interactive confirmation.")
    parser.add_argument("--expire", "-e", type=str, help="Filter by expire date (e.g. '4 September 2026')")
    parser.add_argument("--week", "-w", type=str, help="Filter by week number(s) (e.g. '5' or '1,2,3')")
    parser.add_argument("--ids", "-i", type=str, help="Filter by problem IDs/ranges (e.g. '3129,3155-3167')")
    parser.add_argument("--all", "-a", action="store_true", help="Submit all problems")
    parser.add_argument("--midterm", "-m", action="store_true", help="Select Midterm Exam Course (Course 84)")
    parser.add_argument("--include-learning-log", action="store_true", help="Include Learning Log problems (default: False)")
    parser.add_argument("--recommended-only", action="store_true", help="Only submit recommended problems")
    parser.add_argument("--cookie", "-c", type=str, help="iJudge session cookie")
    parser.add_argument("--cookie-file", type=str, help="Path to cookie text file")
    parser.add_argument("--set-cookie", action="store_true", help="Interactively enter and save a new iJudge cookie")
    parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation prompt and submit immediately")
    parser.add_argument("--dry-run", action="store_true", help="Preview matched problems and files without submitting")
    parser.add_argument("--course-id", type=int, help=f"iJudge Course ID (default: {DEFAULT_COURSE_ID})")
    parser.add_argument("--delay-range", type=str, help="Random delay range between submissions (e.g. '4-6m', '4-6', '240-360s')")
    parser.add_argument("--delay-min", type=str, help="Minimum delay between submissions (e.g. '4m', '240s')")
    parser.add_argument("--delay-max", type=str, help="Maximum delay between submissions (e.g. '6m', '360s')")
    parser.add_argument("--delay-before-first", action="store_true", help="Apply random delay before the first submission as well")

    args = parser.parse_args()

    config = load_config()

    if args.set_cookie:
        prompt_enter_cookie(config)
        return

    # Resolve delay settings
    delay_min = None
    delay_max = None
    if args.delay_range:
        delay_min, delay_max = parse_delay_range_str(args.delay_range)
    if args.delay_min:
        delay_min = parse_delay_val(args.delay_min)
    if args.delay_max:
        delay_max = parse_delay_val(args.delay_max)

    if delay_min is not None and delay_max is None:
        delay_max = delay_min
    elif delay_max is not None and delay_min is None:
        delay_min = delay_max

    if delay_min is not None and delay_max is not None:
        if delay_min > delay_max:
            delay_min, delay_max = delay_max, delay_min

    init_course_id = 84 if args.midterm else (args.course_id or config.get("course_id", DEFAULT_COURSE_ID))
    all_problems = load_all_problems(course_id=init_course_id)

    selected_problems, course_id = filter_problems(all_problems, args, config)

    if not selected_problems:
        print("[!] No problems matched the specified filters.")
        sys.exit(0)

    # If no delay arguments were given on CLI and running interactively, optionally ask for delay
    if delay_min is None and not args.yes and not args.dry_run:
        is_interactive_run = not (args.expire or args.week or args.ids or args.all or args.midterm)
        if is_interactive_run and sys.stdin.isatty():
            try:
                delay_input = input("\nEnter delay range between submissions (e.g. '4-6m' or Enter for none): ").strip()
                if delay_input:
                    d_low, d_high = parse_delay_range_str(delay_input)
                    if d_low is not None:
                        delay_min, delay_max = d_low, d_high
            except (KeyboardInterrupt, EOFError):
                pass

    problem_plans = []
    for p in selected_problems:
        pid = p["id"]
        pname = p.get("name", "")
        file_path = find_solution_file(pid, problem_name=pname)
        file_exists = bool(file_path and os.path.exists(file_path))
        code_content = ""
        warnings = []
        lines_count = 0

        if file_exists:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    code_content = f.read()
                    lines_count = len(code_content.splitlines())
                    warnings = lint_check_code(code_content)
            except Exception as e:
                warnings.append(f"read error: {e}")

        problem_plans.append({
            "problem": p,
            "file_path": file_path,
            "file_exists": file_exists,
            "code": code_content,
            "lines": lines_count,
            "warnings": warnings
        })

    ready_plans = [p for p in problem_plans if p["file_exists"]]
    delay_intervals = []
    total_delay_sec = 0.0
    total_est_duration = 0.0
    start_time = datetime.now()
    finish_time = start_time

    if ready_plans and delay_min is not None and delay_max is not None and delay_max > 0:
        num_intervals = len(ready_plans) if args.delay_before_first else max(0, len(ready_plans) - 1)
        delay_intervals = [random.uniform(delay_min, delay_max) for _ in range(num_intervals)]
        total_delay_sec = sum(delay_intervals)
        overhead_sec = len(ready_plans) * 4.0
        total_est_duration = total_delay_sec + overhead_sec
        finish_time = start_time + timedelta(seconds=total_est_duration)

    print("\n" + "=" * 90)
    course_label = "Course 84 (Midterm)" if course_id == 84 else f"Course {course_id} (Regular)"
    print(f"  iJudge Submission Batch Preview: {course_label} ({len(problem_plans)} problems)")
    print("=" * 90)
    print(f"{'#':<3} | {'OJ ID':<6} | {'Problem Name':<30} | {'Status':<10} | {'File / Warnings'}")
    print("-" * 90)

    ready_count = 0
    for idx, plan in enumerate(problem_plans, 1):
        p = plan["problem"]
        pid = p["id"]
        name = p["name"]
        if plan["file_exists"]:
            rel_path = os.path.relpath(plan["file_path"], PSCP_ROOT)
            if plan["warnings"]:
                status_str = "⚠️ WARNING"
                detail_str = f"{rel_path} ({', '.join(plan['warnings'])})"
            else:
                status_str = "READY"
                detail_str = f"{rel_path} ({plan['lines']} lines)"
            ready_count += 1
        else:
            status_str = "MISSING"
            detail_str = "No solution file found!"

        print(f"{idx:<3d} | OJ {pid:<3d} | {name:<30} | {status_str:<10} | {detail_str}")

    print("-" * 90)
    print(f"Total: {len(problem_plans)} problems | Ready to submit: {ready_count} | Missing: {len(problem_plans) - ready_count}")
    if delay_intervals:
        print("-" * 90)
        print("  Random Delay & Schedule:")
        print(f"  • Interval Range:    {format_time_delta(delay_min)} - {format_time_delta(delay_max)} (randomized)")
        print(f"  • Total Intervals:   {len(delay_intervals)}")
        print(f"  • Total Est. Wait:   ~{format_time_delta(total_delay_sec)}")
        print(f"  • Current Time:      {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  • Est. Finished At:  {finish_time.strftime('%Y-%m-%d %H:%M:%S')} (in ~{format_time_delta(total_est_duration)})")
    print("=" * 90)

    if args.dry_run:
        print("[*] Dry run completed. No submissions were sent.")
        return

    if ready_count == 0:
        print("[!] No solution files available to submit. Aborting.")
        return

    cookie = find_cookie(args.cookie, args.cookie_file, config)
    if not cookie:
        cookie = prompt_enter_cookie(config)

    if not args.yes:
        confirm = input(f"\nSubmit {ready_count} problem(s) to iJudge ({course_label})? [Y/n]: ").strip().lower()
        if confirm not in ("", "y", "yes"):
            print("Submission cancelled.")
            return

    print("\n" + "=" * 90)
    print(f"  Submitting to iJudge ({course_label})...")
    if delay_intervals:
        print(f"  Estimated completion: {finish_time.strftime('%Y-%m-%d %H:%M:%S')} (~{format_time_delta(total_est_duration)} total)")
    print("=" * 90)

    results_summary = []
    actual_course_id = course_id
    delay_interval_idx = 0

    for idx, plan in enumerate(problem_plans, 1):
        p = plan["problem"]
        pid = p["id"]
        name = p["name"]

        if not plan["file_exists"]:
            print(f"[{idx:2d}/{len(problem_plans)}] ❌ OJ {pid:4d} ({name}): Skipped (missing file)")
            results_summary.append({"pid": pid, "name": name, "status": "Skipped", "score": "-", "pep8": "-"})
            continue

        # Check if delay applies before this problem
        should_delay = False
        if delay_intervals:
            if idx == 1 and args.delay_before_first:
                should_delay = True
            elif idx > 1 and delay_interval_idx < len(delay_intervals):
                should_delay = True

        if should_delay:
            d_sec = delay_intervals[delay_interval_idx]
            delay_interval_idx += 1
            cur_batch_rem = max(0, int((finish_time - datetime.now()).total_seconds()))
            finish_str = finish_time.strftime("%H:%M:%S")
            print(f"\n[⏳] Delay before submission {idx}/{len(problem_plans)}: {format_time_delta(d_sec)} wait...")
            cont = run_countdown(d_sec, f"OJ {pid} ({name})", cur_batch_rem, finish_str)
            if not cont:
                print("\n[!] Remaining submissions aborted by user.")
                break

        print(f"[{idx:2d}/{len(problem_plans)}] 📤 Submitting OJ {pid:4d} ({name})...", end="", flush=True)
        try:
            sub_id = submit_problem(pid, plan["code"], cookie, course_id=actual_course_id)
            if not sub_id:
                print(" ❌ Submission Failed (Server rejected request)")
                results_summary.append({"pid": pid, "name": name, "status": "Failed", "score": "-", "pep8": "-"})
                continue

            poll_info = poll_submission_status(sub_id, cookie, poll_timeout=config.get("poll_timeout", 20.0), poll_interval=config.get("poll_interval", 2.0))
            res = poll_info["result"]
            score = poll_info["score"]
            pep8 = poll_info["pep8"]

            is_perfect = (set(res) == {"P"} if res else False) and score == 1000.0
            icon = "✅" if is_perfect else ("⚠️" if set(res) == {"P"} else "❌")

            print(f"\r[{idx:2d}/{len(problem_plans)}] {icon} OJ {pid:4d} ({name:<30}) -> Sub #{sub_id}: {res:<10} | Score: {score:<6.1f} | PEP8: {pep8:<4.1f}")
            results_summary.append({
                "pid": pid,
                "name": name,
                "sub_id": sub_id,
                "result": res,
                "score": f"{score:.1f}",
                "pep8": f"{pep8:.1f}",
                "icon": icon
            })
        except Exception as e:
            print(f" ❌ Error: {e}")
            results_summary.append({"pid": pid, "name": name, "status": f"Error: {e}", "score": "-", "pep8": "-"})

        time.sleep(1.0)

    print("\n" + "=" * 90)
    print(f"  Submission Summary Report ({course_label})")
    print("=" * 90)
    print(f"{'#':<3} | {'OJ ID':<6} | {'Problem Name':<30} | {'Sub ID':<7} | {'Result':<10} | {'Score':<7} | {'PEP8':<6}")
    print("-" * 90)
    for idx, r in enumerate(results_summary, 1):
        icon = r.get("icon", "  ")
        sub_id = str(r.get("sub_id", "-"))
        res = r.get("result", r.get("status", "-"))
        print(f"{idx:<3d} | OJ {r['pid']:<3d} | {r['name']:<30} | #{sub_id:<6} | {icon} {res:<7} | {r.get('score', '-'):<7} | {r.get('pep8', '-'):<6}")
    print("=" * 90)
    elapsed_total = (datetime.now() - start_time).total_seconds()
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Total elapsed: {format_time_delta(elapsed_total)})")


if __name__ == "__main__":
    main()
