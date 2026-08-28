#!/usr/bin/env python3
"""
Standardized CLI tool to submit PSCP OJ problems to iJudge.

Features:
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
import re
import sys
import time
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PSCP_ROOT = os.path.dirname(SCRIPT_DIR)
WORKSPACE_ROOT = os.path.dirname(PSCP_ROOT)
CONFIG_FILE = os.path.join(PSCP_ROOT, "submit_config.json")
PROBLEMS_JSON = os.path.join(PSCP_ROOT, "oj_problems.json")
OJ_DIR = os.path.join(PSCP_ROOT, "oj")

DEFAULT_COURSE_ID = 78
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:153.0) Gecko/20100101 Firefox/153.0",
    "Accept": "text/x-component",
    "Content-Type": "text/plain;charset=UTF-8",
    "next-action": "7fc32d2dd54d0b8574db835d9b74354be0cac2fbd7",
    "Origin": "https://ijudge.it.kmitl.ac.th"
}


def load_config():
    """Load configuration from submit_config.json if it exists."""
    config = {
        "course_id": DEFAULT_COURSE_ID,
        "exclude_learning_logs": True,
        "poll_interval": 2.0,
        "poll_timeout": 15.0,
        "cookie": ""
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                user_conf = json.load(f)
                config.update(user_conf)
        except Exception as e:
            print(f"[!] Warning: Failed to parse {CONFIG_FILE}: {e}")
    return config


def save_config(config):
    """Save configuration to submit_config.json."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"[*] Configuration saved to {CONFIG_FILE}")
    except Exception as e:
        print(f"[!] Warning: Failed to save {CONFIG_FILE}: {e}")


def validate_cookie(cookie):
    """Validate iJudge cookie against submissions endpoint and return user profile info."""
    if not cookie or not cookie.strip():
        return {"valid": False, "username": None, "fullname": None, "error": "Empty cookie"}

    url = "https://ijudge.it.kmitl.ac.th/submissions/me"
    headers = {
        "User-Agent": DEFAULT_HEADERS["User-Agent"],
        "Accept": "*/*",
        "rsc": "1",
        "Cookie": cookie
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8")
        m_user = re.search(r"\"username\":\"([^\"]+)\"", body)
        m_name = re.search(r"\"fullname\":\"([^\"]+)\"", body)
        if m_user:
            return {
                "valid": True,
                "username": m_user.group(1),
                "fullname": m_name.group(1) if m_name else "",
                "error": None
            }
        return {"valid": False, "username": None, "fullname": None, "error": "Not authenticated (invalid session)"}
    except Exception as e:
        return {"valid": False, "username": None, "fullname": None, "error": str(e)}


def find_cookie(cli_cookie=None, cli_cookie_file=None, config=None):
    """Resolve iJudge session cookie from various potential sources."""
    # 1. CLI direct string
    if cli_cookie and cli_cookie.strip():
        return cli_cookie.strip()

    # 2. CLI cookie file
    if cli_cookie_file and os.path.exists(cli_cookie_file):
        try:
            with open(cli_cookie_file, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception:
            pass

    # 3. Environment Variable
    env_cookie = os.environ.get("IJUDGE_COOKIE")
    if env_cookie and env_cookie.strip():
        return env_cookie.strip()

    # 4. Config file
    if config and config.get("cookie", "").strip():
        return config["cookie"].strip()

    # 5. .ijudge_cookie in workspace or pscp root
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

    # 6. Check .env / .env.local
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

    # Validate
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


def load_all_problems():
    """Load oj_problems.json."""
    if not os.path.exists(PROBLEMS_JSON):
        print(f"[!] Error: {PROBLEMS_JSON} not found.")
        sys.exit(1)
    with open(PROBLEMS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def find_solution_file(problem_id):
    """Locate the Python solution file for a problem."""
    # Check oj/oj<id>-* directories
    for path in glob.glob(os.path.join(OJ_DIR, f"oj{problem_id}-*")):
        if os.path.isdir(path):
            main_py = os.path.join(path, "main.py")
            if os.path.exists(main_py):
                return main_py

    # Check root-level oj<id> directories
    root_oj = os.path.join(PSCP_ROOT, f"oj{problem_id}")
    if os.path.isdir(root_oj):
        main_py = os.path.join(root_oj, "main.py")
        if os.path.exists(main_py):
            return main_py

    # Check loose files
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

    # Filter by specific IDs
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

    # Filter by Expire Date
    elif args.expire:
        query = args.expire.strip().lower()
        filtered = [p for p in all_problems if query in p.get("expire_date", "").lower()]

    # Filter by Week
    elif args.week is not None:
        target_weeks = set()
        for token in str(args.week).split(","):
            if token.strip().isdigit():
                target_weeks.add(int(token.strip()))
        filtered = [p for p in all_problems if p.get("week") in target_weeks]

    # Filter by All
    elif args.all:
        filtered = list(all_problems)

    # Interactive Menu
    else:
        filtered = interactive_selection_menu(all_problems, config)

    # Apply Learning Log exclusion
    if exclude_ll:
        filtered = [p for p in filtered if not p.get("is_learning_log", False) and "Learning Log" not in p.get("name", "")]

    # Apply Recommended filter
    if getattr(args, "recommended_only", False):
        filtered = [p for p in filtered if p.get("is_recommended", False)]

    # Sort by ID
    filtered.sort(key=lambda p: p.get("id", 0))
    return filtered


def interactive_selection_menu(all_problems, config):
    """Render interactive CLI menu to pick problem batch or configure cookie."""
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

        print("\n" + "=" * 65)
        print("  PSCP iJudge Submission Tool")
        print(f"  Status: {auth_status}")
        print("=" * 65)

        # Group by expire dates
        expire_groups = {}
        for p in all_problems:
            exp = p.get("expire_date") or "No Expire Date"
            expire_groups.setdefault(exp, []).append(p)

        sorted_dates = sorted(expire_groups.keys(), key=lambda d: ("1" if "2026" in d else "2", d))

        print("Options:")
        for idx, d in enumerate(sorted_dates, 1):
            count = len(expire_groups[d])
            ll_count = sum(1 for p in expire_groups[d] if p.get("is_learning_log"))
            print(f"  [{idx:2d}] Expire: {d:<26} ({count} problems, {ll_count} Learning Logs)")
        
        print(f"  [ W] Filter by Week (e.g. Week 1, 2, 3)")
        print(f"  [ I] Enter Specific Problem IDs / Ranges (e.g. 3155-3167, 3129)")
        print(f"  [ A] All Problems ({len(all_problems)} total)")
        print(f"  [ C] Enter / Update iJudge Cookie")
        print(f"  [ Q] Quit")
        print("-" * 65)

        choice = input("Enter your choice: ").strip()
        if not choice or choice.lower() == "q":
            print("Aborted.")
            sys.exit(0)

        if choice.lower() == "c":
            prompt_enter_cookie(config)
            continue

        if choice.isdigit() and 1 <= int(choice) <= len(sorted_dates):
            selected_date = sorted_dates[int(choice) - 1]
            return expire_groups[selected_date]
        elif choice.lower() == "w":
            weeks_str = input("Enter week numbers separated by comma (e.g. 1, 2, 5): ").strip()
            weeks = {int(w.strip()) for w in weeks_str.split(",") if w.strip().isdigit()}
            return [p for p in all_problems if p.get("week") in weeks]
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
            return [p for p in all_problems if p.get("id") in target_ids]
        elif choice.lower() == "a":
            return list(all_problems)
        else:
            print("[!] Invalid choice. Please try again.")


def submit_problem(problem_id, code, cookie, course_id=DEFAULT_COURSE_ID):
    """Submit a single problem to iJudge."""
    url = f"https://ijudge.it.kmitl.ac.th/problems/{problem_id}/description?problemPage=0"
    payload = json.dumps([{
        "code": code,
        "lang_type": "Python",
        "course_problem_id": problem_id,
        "course_id": course_id
    }]).encode("utf-8")

    headers = dict(DEFAULT_HEADERS)
    headers["Cookie"] = cookie
    headers["Referer"] = url

    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = resp.read().decode("utf-8")

    m_sub = re.search(r"\"submissionId\":\s*(\d+)", body)
    if m_sub:
        return int(m_sub.group(1))
    return None


def poll_submission_status(submission_id, cookie, poll_timeout=15.0, poll_interval=2.0):
    """Poll iJudge overview endpoint to retrieve submission result and PEP8 score."""
    url = f"https://ijudge.it.kmitl.ac.th/submissions/{submission_id}/overview"
    headers = {
        "User-Agent": DEFAULT_HEADERS["User-Agent"],
        "Accept": "*/*",
        "rsc": "1",
        "Cookie": cookie
    }

    start_time = time.time()
    while time.time() - start_time < poll_timeout:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = resp.read().decode("utf-8")

            m_res = re.search(r"\"result\":\"([^\"]+)\"", body)
            m_score = re.search(r"\"score\":([\d\.]+)", body)
            m_pep8 = re.search(r"\"pep8_score\":([\d\.]+)", body)

            if m_res and m_res.group(1) != "null":
                result = m_res.group(1)
                score = float(m_score.group(1)) if m_score else 0.0
                pep8 = float(m_pep8.group(1)) if m_pep8 else 0.0
                return {"result": result, "score": score, "pep8": pep8, "ready": True}
        except Exception:
            pass
        time.sleep(poll_interval)

    return {"result": "Pending", "score": 0.0, "pep8": 0.0, "ready": False}


def main():
    parser = argparse.ArgumentParser(description="Submit PSCP OJ problems to iJudge with interactive confirmation.")
    parser.add_argument("--expire", "-e", type=str, help="Filter by expire date (e.g. '4 September 2026')")
    parser.add_argument("--week", "-w", type=str, help="Filter by week number(s) (e.g. '5' or '1,2,3')")
    parser.add_argument("--ids", "-i", type=str, help="Filter by problem IDs/ranges (e.g. '3129,3155-3167')")
    parser.add_argument("--all", "-a", action="store_true", help="Submit all problems")
    parser.add_argument("--include-learning-log", action="store_true", help="Include Learning Log problems (default: False)")
    parser.add_argument("--recommended-only", action="store_true", help="Only submit recommended problems")
    parser.add_argument("--cookie", "-c", type=str, help="iJudge session cookie")
    parser.add_argument("--cookie-file", type=str, help="Path to cookie text file")
    parser.add_argument("--set-cookie", action="store_true", help="Interactively enter and save a new iJudge cookie")
    parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation prompt and submit immediately")
    parser.add_argument("--dry-run", action="store_true", help="Preview matched problems and files without submitting")
    parser.add_argument("--course-id", type=int, default=DEFAULT_COURSE_ID, help=f"iJudge Course ID (default: {DEFAULT_COURSE_ID})")

    args = parser.parse_args()

    config = load_config()

    # Handle direct cookie update flag
    if args.set_cookie:
        prompt_enter_cookie(config)
        return

    all_problems = load_all_problems()

    # Determine problems to submit
    selected_problems = filter_problems(all_problems, args, config)

    if not selected_problems:
        print("[!] No problems matched the specified filters.")
        sys.exit(0)

    # Locate solution files and inspect for lint warnings
    problem_plans = []
    for p in selected_problems:
        pid = p["id"]
        file_path = find_solution_file(pid)
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

    # Render Preview Table
    print("\n" + "=" * 90)
    print(f"  iJudge Submission Batch Preview ({len(problem_plans)} problems)")
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
    print("=" * 90)

    if args.dry_run:
        print("[*] Dry run completed. No submissions were sent.")
        return

    if ready_count == 0:
        print("[!] No solution files available to submit. Aborting.")
        return

    # Obtain and validate Cookie
    cookie = find_cookie(args.cookie, args.cookie_file, config)
    if not cookie:
        cookie = prompt_enter_cookie(config)

    # Prompt Confirmation
    if not args.yes:
        confirm = input(f"\nSubmit {ready_count} problem(s) to iJudge? [Y/n]: ").strip().lower()
        if confirm not in ("", "y", "yes"):
            print("Submission cancelled.")
            return

    # Execute Submissions
    print("\n" + "=" * 90)
    print("  Submitting to iJudge...")
    print("=" * 90)

    results_summary = []
    course_id = args.course_id or config.get("course_id", DEFAULT_COURSE_ID)

    for idx, plan in enumerate(problem_plans, 1):
        p = plan["problem"]
        pid = p["id"]
        name = p["name"]

        if not plan["file_exists"]:
            print(f"[{idx:2d}/{len(problem_plans)}] ❌ OJ {pid:4d} ({name}): Skipped (missing file)")
            results_summary.append({"pid": pid, "name": name, "status": "Skipped", "score": "-", "pep8": "-"})
            continue

        print(f"[{idx:2d}/{len(problem_plans)}] 📤 Submitting OJ {pid:4d} ({name})...", end="", flush=True)
        try:
            sub_id = submit_problem(pid, plan["code"], cookie, course_id=course_id)
            if not sub_id:
                print(" ❌ Submission Failed (Server rejected request)")
                results_summary.append({"pid": pid, "name": name, "status": "Failed", "score": "-", "pep8": "-"})
                continue

            # Poll for result
            poll_info = poll_submission_status(sub_id, cookie, poll_timeout=config.get("poll_timeout", 15.0), poll_interval=config.get("poll_interval", 2.0))
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

        # Short pause between submissions
        time.sleep(1.0)

    # Final Summary Table
    print("\n" + "=" * 90)
    print("  Submission Summary Report")
    print("=" * 90)
    print(f"{'#':<3} | {'OJ ID':<6} | {'Problem Name':<30} | {'Sub ID':<7} | {'Result':<10} | {'Score':<7} | {'PEP8':<6}")
    print("-" * 90)
    for idx, r in enumerate(results_summary, 1):
        icon = r.get("icon", "  ")
        sub_id = str(r.get("sub_id", "-"))
        res = r.get("result", r.get("status", "-"))
        print(f"{idx:<3d} | OJ {r['pid']:<3d} | {r['name']:<30} | #{sub_id:<6} | {icon} {res:<7} | {r.get('score', '-'):<7} | {r.get('pep8', '-'):<6}")
    print("=" * 90)
    print("Done!")


if __name__ == "__main__":
    main()
