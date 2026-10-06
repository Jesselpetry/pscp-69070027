#!/usr/bin/env python3
"""
Generate README.md and refresh oj_problems.json for pscp-69070027 (and the ihelp
mirror) from the scraped registries plus metadata recovered from git history.

The README gets the progress dashboard, the repository layout, the state of the
main / solutions branches, and per-week problem tables with folder and file
links. The planned restructure of this pipeline is tracked in docs/PLAN.md.
"""

import json
import os
import re
import subprocess
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ijudge import get_week  # noqa: E402

PSCP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README_PATH = os.path.join(PSCP_ROOT, "README.md")
DETAIL_JSON = os.path.join(PSCP_ROOT, "data", "all_problems_detail.json")
OJ_PROBLEMS_PSCP = os.path.join(PSCP_ROOT, "oj_problems.json")

IHELP_ROOT = os.path.normpath(os.path.join(PSCP_ROOT, "..", "ihelp"))
OJ_PROBLEMS_IHELP = os.path.join(IHELP_ROOT, "data", "oj_problems.json")

HTML_CACHE_DIR = os.path.join(PSCP_ROOT, "data", "html_cache")
PLAN_PATH = os.path.join(PSCP_ROOT, "docs", "PLAN.md")
WORK_BRANCH = "main"
SOLUTIONS_BRANCH = "solutions/2026-s1"
ARCHIVE_WORKTREE = ".pscp-archive"

def url_quote(path):
    return urllib.parse.quote(path)


def git_out(*args):
    """Run git in the repo and return stdout, or "" when the command fails."""
    try:
        return subprocess.check_output(
            ["git", *args], cwd=PSCP_ROOT, stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def count_entries(path, predicate=os.path.isdir):
    """Number of entries under `path` matching `predicate` (0 if it is missing)."""
    if not os.path.isdir(path):
        return 0
    return sum(1 for d in os.listdir(path) if predicate(os.path.join(path, d)))


def branch_status_lines():
    """README lines comparing the working branch with the solutions archive.

    Reflects the local refs at generation time, so regenerate after committing
    or pulling for the numbers to be current.
    """
    branches = [
        (WORK_BRANCH, "Workspace: `problem.md` + `main.py` (โจทย์ใหม่เป็น stub) + scripts + data"),
        (SOLUTIONS_BRANCH, f"คลังโค้ดที่ทำเสร็จแล้ว — checkout เป็น worktree `{ARCHIVE_WORKTREE}/` (gitignored)"),
    ]
    existing = [(b, role) for b, role in branches if git_out("rev-parse", "--verify", "--quiet", b)]
    if not existing:
        return []

    ahead = {}
    if len(existing) == 2:
        counts = git_out("rev-list", "--left-right", "--count", f"{WORK_BRANCH}...{SOLUTIONS_BRANCH}").split()
        if len(counts) == 2:
            ahead = {WORK_BRANCH: counts[0], SOLUTIONS_BRANCH: counts[1]}

    lines = [
        "| Branch | บทบาท | Commit ล่าสุด | นำอีก branch | ยังไม่ push |",
        "| :--- | :--- | :--- | :---: | :---: |",
    ]
    for branch, role in existing:
        last = git_out("log", "-1", "--format=%h %cs", branch) or "-"
        sha, _, date = last.partition(" ")
        unpushed = git_out("rev-list", "--count", f"origin/{branch}..{branch}") or "-"
        lines.append(
            f"| `{branch}` | {role} | `{sha}` · {date} | {ahead.get(branch, '-')} | {unpushed} |"
        )
    lines.append("")
    if ahead and ahead[WORK_BRANCH] != "0" and ahead[SOLUTIONS_BRANCH] != "0":
        lines.append(
            "> ⚠️ สอง branch แยกทางกัน (diverged) — ต้องรวมโค้ดก่อนใช้ "
            f"`{SOLUTIONS_BRANCH}` เป็นต้นฉบับ"
            + (" ดูขั้นตอนใน [`docs/PLAN.md`](docs/PLAN.md)" if os.path.exists(PLAN_PATH) else "")
        )
        lines.append("")
    return lines

WEEK_TITLES = {
    1: "Week 1: บทนำ ตัวแปร และการรับส่งข้อมูลพื้นฐาน (Basic I/O & Variables)",
    2: "Week 2: การทำงานแบบมีเงื่อนไขพื้นฐาน (Basic Conditionals & Logic)",
    3: "Week 3: การทำงานแบบมีเงื่อนไขขั้นสูง (Nested Conditionals & Advanced Logic)",
    4: "Week 4: การทำงานซ้ำแบบ While Loop และตัวแปรสะสม (While Loops & Accumulators)",
    5: "Week 5: การทำงานซ้ำแบบ For Loop และลูปซ้อนลูป (For Loops & Geometry Drawing)",
    6: "Week 6: ลูปขั้นสูง สตริง และลำดับอนุกรม (Advanced Loops, Strings & Sequences)",
    7: "Week 7 / Midterm: ชุดข้อสอบจำลองกลางภาค (Midterm Mock Exam)",
    8: "Week 8: ลิสต์และการประมวลผลสตริงขั้นสูง (Lists & Advanced Sequence Operations)",
    9: "Week 9: ลิสต์ขั้นสูงและการประยุกต์ใช้งาน (Advanced Lists & Applied Algorithms)",
    10: "Week 10: ทูเพิล ลิสต์ 2 มิติ และการเรียงลำดับ (Tuples, 2D Lists & Sorting)",
    11: "Week 11: การจำลองการทำงานและเซต (Simulation, String Processing & Sets)",
    12: "Week 12: ดิกชันนารีและเซตขั้นสูง (Advanced Dictionaries, Sets & Algorithms)",
    13: "Week 13: การเรียกซ้ำ (Recursion & Divide and Conquer)",
    14: "Week 14: ชุดข้อสอบย่อยจำลอง (Mini Exam / Mock Test)",
}

def load_master_metadata():
    meta_db = {}
    
    # 1. Recover historical metadata from git history
    try:
        commit_hashes = subprocess.check_output(
            ["git", "log", "--format=%H", "--", "oj_problems.json"], cwd=PSCP_ROOT
        ).decode("utf-8").splitlines()
        
        for h in reversed(commit_hashes):
            try:
                raw = subprocess.check_output(
                    ["git", "show", f"{h}:oj_problems.json"], cwd=PSCP_ROOT
                ).decode("utf-8")
                arr = json.loads(raw)
                for item in arr:
                    pid = item["id"]
                    if pid not in meta_db or item.get("passed_count", 0) > meta_db[pid].get("passed_count", 0):
                        meta_db[pid] = item
            except Exception:
                pass
    except Exception:
        pass

    # 2. Update with active scraped details
    if os.path.exists(DETAIL_JSON):
        with open(DETAIL_JSON, "r", encoding="utf-8") as f:
            active_details = json.load(f)
        for p in active_details:
            pid = p["id"]
            meta_db[pid] = {
                "id": pid,
                "name": p["name"],
                "status": p["status"],
                "difficulty": p["difficulty"],
                "passed_count": p["passed_count"],
                "attempt_count": p["attempt_count"],
                "percentage": p["percentage"],
                "expire_date": p["expire_date"],
                "is_learning_log": p["is_learning_log"],
                "is_recommended": p["is_recommended"],
                "is_midterm": p.get("is_midterm", False),
                "is_mini_exam": p.get("is_mini_exam", False),
                "url": p["url"]
            }

    # 3. Load active summary registry for any problems not yet in detail
    if os.path.exists(OJ_PROBLEMS_PSCP):
        with open(OJ_PROBLEMS_PSCP, "r", encoding="utf-8") as f:
            for item in json.load(f):
                pid = item["id"]
                if pid not in meta_db:
                    meta_db[pid] = item

    # 4. Assign week
    for pid, item in meta_db.items():
        item["week"] = get_week(item)
        
    return meta_db

def generate_readme():
    meta_db = load_master_metadata()

    root_oj = [d for d in os.listdir(PSCP_ROOT) if d.startswith("oj") and d != "oj" and os.path.isdir(os.path.join(PSCP_ROOT, d))]
    oj_dir = os.path.join(PSCP_ROOT, "oj")
    oj_sub = [d for d in os.listdir(oj_dir) if os.path.isdir(os.path.join(oj_dir, d))] if os.path.exists(oj_dir) else []
    rec_dir = os.path.join(PSCP_ROOT, "recommended")
    rec_sub = [d for d in os.listdir(rec_dir) if os.path.isdir(os.path.join(rec_dir, d))] if os.path.exists(rec_dir) else []

    all_ids = sorted(list(set(
        list(meta_db.keys()) +
        [int(re.match(r"oj(\d+)", d).group(1)) for d in root_oj if re.match(r"oj(\d+)", d)] +
        [int(re.match(r"oj(\d+)", d).group(1)) for d in oj_sub if re.match(r"oj(\d+)", d)] +
        [int(re.match(r"oj(\d+)", d).group(1)) for d in rec_sub if re.match(r"oj(\d+)", d)]
    )))

    records = []
    for pid in all_ids:
        meta = meta_db.get(pid, {})
        r_dirs = [d for d in root_oj if d == f"oj{pid}"]
        o_dirs = [d for d in oj_sub if d.startswith(f"oj{pid}-") or d == f"oj{pid}"]
        rec_dirs = [d for d in rec_sub if d.startswith(f"oj{pid}-") or d == f"oj{pid}"]
        
        name = meta.get("name", "")
        if not name:
            if rec_dirs:
                name = rec_dirs[0].replace(f"oj{pid}-", "").replace("_", " ")
            elif o_dirs:
                name = o_dirs[0].replace(f"oj{pid}-", "").replace(" ✅", "").replace("_", " ")
            elif r_dirs:
                name = f"Learning Log {pid}"
            
        is_passed = False
        if meta.get("status") == "Passed":
            is_passed = True
        elif any("✅" in d for d in o_dirs):
            is_passed = True
        elif r_dirs and os.path.exists(os.path.join(PSCP_ROOT, r_dirs[0], "submission.md")):
            with open(os.path.join(PSCP_ROOT, r_dirs[0], "submission.md"), "r", encoding="utf-8", errors="ignore") as f:
                if "Pass" in f.read():
                    is_passed = True
                    
        is_rec = meta.get("is_recommended", False) or len(rec_dirs) > 0
        is_ll = meta.get("is_learning_log", False) or len(r_dirs) > 0
        is_mid = meta.get("is_midterm", False) or "[ MIDTERM ]" in name.upper() or (3274 <= pid <= 3282)
        is_mini = meta.get("is_mini_exam", False) or "MINI EXAM" in name.upper() or (3489 <= pid <= 3511) or (3546 <= pid <= 3551)
        week = meta.get("week") or get_week({"id": pid, "name": name, "expire_date": meta.get("expire_date", "")})
        
        records.append({
            "id": pid,
            "name": name,
            "week": week,
            "is_passed": is_passed,
            "is_rec": is_rec,
            "is_ll": is_ll,
            "is_midterm": is_mid,
            "is_mini_exam": is_mini,
            "root_dir": r_dirs[0] if r_dirs else None,
            "oj_dir": o_dirs[0] if o_dirs else None,
            "rec_dir": rec_dirs[0] if rec_dirs else None,
            "meta": meta
        })

    # Save complete oj_problems.json
    summary_list = []
    for r in records:
        m = r.get("meta") or {}
        summary_list.append({
            "id": r["id"],
            "name": r["name"],
            "week": r["week"],
            "status": "Passed" if r["is_passed"] else (m.get("status", "Not Passed")),
            "difficulty": m.get("difficulty", 0),
            "passed_count": m.get("passed_count", 0),
            "attempt_count": m.get("attempt_count", 0),
            "percentage": m.get("percentage", 0.0),
            "expire_date": m.get("expire_date", ""),
            "is_learning_log": r["is_ll"],
            "is_recommended": r["is_rec"],
            "is_midterm": r["is_midterm"],
            "is_mini_exam": r["is_mini_exam"],
            "url": m.get("url", f"https://ijudge.it.kmitl.ac.th/problems/{r['id']}/description")
        })

    with open(OJ_PROBLEMS_PSCP, "w", encoding="utf-8") as f:
        json.dump(summary_list, f, indent=2, ensure_ascii=False)
    if os.path.exists(os.path.dirname(OJ_PROBLEMS_IHELP)):
        with open(OJ_PROBLEMS_IHELP, "w", encoding="utf-8") as f:
            json.dump(summary_list, f, indent=2, ensure_ascii=False)
    print(f"Saved complete oj_problems.json ({len(summary_list)} problems) with full historical stats & weeks.")

    total_count = len(records)
    passed_count = sum(1 for r in records if r["is_passed"])
    in_prog_count = total_count - passed_count
    pass_pct = (passed_count / total_count * 100) if total_count else 0

    lines = []
    lines.append('<div align="center">')
    lines.append('  <img src="public/IT-KMITL-Logo.png" alt="IT KMITL Logo" width="420"/>')
    lines.append('</div>')
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("# PSCP — Problem Solving and Computer Programming")
    lines.append("")
    lines.append("**การแก้ปัญหาและการโปรแกรมคอมพิวเตอร์ (06066303)**")
    lines.append("3 Credits (2-2-5) · Bachelor's Degree · School of Information Technology, KMITL")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 👤 Student Information")
    lines.append("")
    lines.append("| Field | Details |")
    lines.append("| :--- | :---|")
    lines.append("| **Name (TH)** | นายฉัททัณฑ์ เพททริ |")
    lines.append("| **Name (EN)** | Chatan Petry |")
    lines.append("| **Student ID** | 69070027 |")
    lines.append("| **Email** | 69070027@kmitl.ac.th |")
    lines.append("| **Faculty** | คณะเทคโนโลยีสารสนเทศ (School of Information Technology) |")
    lines.append("| **Institution** | สถาบันเทคโนโลยีพระจอมเกล้าเจ้าคุณทหารลาดกระบัง (KMITL) |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📊 Overall Progress Dashboard")
    lines.append("")
    lines.append(f"- **Total Problems Tracked**: `{total_count}`")
    lines.append(f"- **✅ Solved / Passed**: `{passed_count}` ({pass_pct:.1f}%)")
    lines.append(f"- **🔄 In Progress / Pending**: `{in_prog_count}`")
    lines.append("")
    lines.append("### 📅 Weekly Progress (นับตั้งแต่สัปดาห์แรกที่เปิดเทอม)")
    lines.append("")
    lines.append("| Week | Topic / Focus | Total | Passed | In Progress | Completion |")
    lines.append("| :---: | :--- | :---: | :---: | :---: | :---: |")
    active_weeks = sorted(list(set(r["week"] for r in records if r["week"] in WEEK_TITLES)))
    for w in active_weeks:
        w_records = [r for r in records if r["week"] == w]
        w_pass = sum(1 for r in w_records if r["is_passed"])
        w_pend = len(w_records) - w_pass
        w_pct = (w_pass / len(w_records) * 100) if w_records else 0
        w_title = WEEK_TITLES[w].split(":", 1)[1].strip()
        lines.append(f"| **Week {w}** | {w_title} | {len(w_records)} | {w_pass} | {w_pend} | **{w_pct:.1f}%** |")
    lines.append("")
    lines.append("### 🏷️ Category Breakdown")
    lines.append("")
    lines.append("| Category | Total | Passed | In Progress |")
    lines.append("| :--- | :---: | :---: | :---: |")
    
    mid_records = [r for r in records if r["is_midterm"]]
    mini_records = [r for r in records if r["is_mini_exam"]]
    rec_records = [r for r in records if r["is_rec"]]
    ll_records = [r for r in records if r["is_ll"]]
    
    lines.append(f"| **🎯 Midterm Mock Exam** | {len(mid_records)} | {sum(1 for r in mid_records if r['is_passed'])} | {sum(1 for r in mid_records if not r['is_passed'])} |")
    lines.append(f"| **📝 Mini Exam** | {len(mini_records)} | {sum(1 for r in mini_records if r['is_passed'])} | {sum(1 for r in mini_records if not r['is_passed'])} |")
    lines.append(f"| **🌟 Recommended Problems** | {len(rec_records)} | {sum(1 for r in rec_records if r['is_passed'])} | {sum(1 for r in rec_records if not r['is_passed'])} |")
    lines.append(f"| **📓 Learning Logs** | {len(ll_records)} | {sum(1 for r in ll_records if r['is_passed'])} | {sum(1 for r in ll_records if not r['is_passed'])} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    html_cache_count = count_entries(HTML_CACHE_DIR, os.path.isfile)
    rec_folder_count = len([d for d in rec_sub if re.match(r"oj\d+", d)])
    has_plan = os.path.exists(PLAN_PATH)

    lines.append("## 📁 Repository Structure")
    lines.append("")
    lines.append("```")
    lines.append("pscp-69070027/")
    lines.append(f"├── oj/                          # โจทย์ปกติ + Midterm + Mini Exam ({len(oj_sub)} โฟลเดอร์): oj<id>-<Name>/ → problem.md, main.py")
    lines.append(f"├── oj<id>/                      # Learning Log ({len(root_oj)} โฟลเดอร์): main.py, problem.md, submission.md")
    lines.append(f"├── recommended/                 # สำเนาโจทย์แนะนำ ({rec_folder_count} ข้อ) + สรุป ce-kmitl")
    lines.append("├── oj_problems.json             # registry สรุป: id, week, status, flags")
    lines.append("├── data/")
    lines.append("│   ├── all_problems_detail.json # registry ละเอียด: โจทย์, sample, limits")
    lines.append("│   ├── course_84_problems.json  # โจทย์ Midterm (course 84)")
    lines.append(f"│   └── html_cache/              # HTML ดิบ {html_cache_count} หน้า (gitignored)")
    lines.append("├── scripts/                     # scrape / submit / sync / สร้าง README")
    if has_plan:
        lines.append("├── docs/PLAN.md                 # แผนจัดระเบียบ repo")
    lines.append("└── AI-Guidelines-PSCP/          # แนวทางการใช้ AI ของรายวิชา")
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")

    branch_lines = branch_status_lines()
    if branch_lines:
        lines.append("## 🌿 Branches")
        lines.append("")
        lines.extend(branch_lines)
        lines.append("```bash")
        lines.append(f"git worktree add {ARCHIVE_WORKTREE} {SOLUTIONS_BRANCH}   # ครั้งเดียว ถ้ายังไม่มี")
        lines.append(f"git show {SOLUTIONS_BRANCH}:\"oj/oj2981-Sawasdee_Name ✅/main.py\"   # ดูโค้ดใน archive")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Section 1: Midterm Mock Exam
    lines.append("## 🎯 1. Midterm Mock Exam Problems (Week 7)")
    lines.append("")
    lines.append("ชุดข้อสอบจำลอง Midterm PSCP พร้อมคำอธิบายโจทย์ ข้อกำหนด และตัวอย่างเทสเคส")
    lines.append("")
    lines.append("| OJ ID | Problem Name | Status | Problem Folder | Problem Spec | Solution Code |")
    lines.append("| :---: | :--- | :---: | :--- | :---: | :---: |")
    for r in mid_records:
        pid = r["id"]
        p_name = r["name"]
        stat_badge = "✅ **Passed**" if r["is_passed"] else "🔄 *In Progress*"
        folder_link = f"[`{r['oj_dir']}`](oj/{url_quote(r['oj_dir'])})" if r["oj_dir"] else "-"
        md_link = f"[`problem.md`](oj/{url_quote(r['oj_dir'])}/problem.md)" if r["oj_dir"] and os.path.exists(os.path.join(PSCP_ROOT, "oj", r["oj_dir"], "problem.md")) else "-"
        code_link = f"[`main.py`](oj/{url_quote(r['oj_dir'])}/main.py)" if r["oj_dir"] and os.path.exists(os.path.join(PSCP_ROOT, "oj", r["oj_dir"], "main.py")) else "-"
        lines.append(f"| **{pid}** | {p_name} | {stat_badge} | {folder_link} | {md_link} | {code_link} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 2: Recommended Problems
    lines.append(f"## 🌟 2. Recommended Problems (คลังโจทย์แนะนำ {len(rec_records)} ข้อ)")
    lines.append("")
    lines.append(f"โจทย์สำคัญ {len(rec_records)} ข้อที่รวบรวมเทคนิคสำคัญของภาษา Python พร้อมคำอธิบายและแนวคิดอย่างละเอียด")
    lines.append("")
    lines.append("| OJ ID | Problem Name | Week | Status | Recommended Folder | Standard Folder | Problem Spec | Solution Code |")
    lines.append("| :---: | :--- | :---: | :---: | :--- | :--- | :---: | :---: |")
    for r in rec_records:
        pid = r["id"]
        p_name = r["name"]
        w = r["week"]
        stat_badge = "✅ **Passed**" if r["is_passed"] else "🔄 *In Progress*"
        rec_folder_link = f"[`{r['rec_dir']}`](recommended/{url_quote(r['rec_dir'])})" if r["rec_dir"] else "-"
        oj_folder_link = f"[`{r['oj_dir']}`](oj/{url_quote(r['oj_dir'])})" if r["oj_dir"] else (f"[`{r['root_dir']}`]({url_quote(r['root_dir'])})" if r["root_dir"] else "-")
        
        md_path = f"recommended/{url_quote(r['rec_dir'])}/problem.md" if r["rec_dir"] else "-"
        md_link = f"[`problem.md`]({md_path})" if md_path != "-" else "-"
        
        code_path = f"recommended/{url_quote(r['rec_dir'])}/main.py" if r["rec_dir"] else "-"
        code_link = f"[`main.py`]({code_path})" if code_path != "-" else "-"
        
        lines.append(f"| **{pid}** | {p_name} | Week {w} | {stat_badge} | {rec_folder_link} | {oj_folder_link} | {md_link} | {code_link} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 3: Learning Logs
    lines.append("## 📓 3. Learning Logs (บันทึกการเรียนรู้)")
    lines.append("")
    lines.append("โจทย์ที่ต้องส่ง Learning Log พร้อมบันทึก `submission.md` และการสะท้อนความคิด")
    lines.append("")
    lines.append("| OJ ID | Problem Name | Week | Status | Learning Log Folder | Problem Spec | Submission Doc | Code |")
    lines.append("| :---: | :--- | :---: | :---: | :--- | :---: | :---: | :---: |")
    for r in ll_records:
        pid = r["id"]
        p_name = r["name"]
        w = r["week"]
        stat_badge = "✅ **Passed**" if r["is_passed"] else "🔄 *In Progress*"
        
        root_d = r["root_dir"] if r["root_dir"] else f"oj{pid}"
        has_root_dir = os.path.exists(os.path.join(PSCP_ROOT, root_d))
        folder_link = f"[`{root_d}`]({url_quote(root_d)})" if has_root_dir else (f"[`{r['oj_dir']}`](oj/{url_quote(r['oj_dir'])})" if r["oj_dir"] else "-")
        
        spec_link = "-"
        if has_root_dir and os.path.exists(os.path.join(PSCP_ROOT, root_d, "problem.md")):
            spec_link = f"[`problem.md`]({url_quote(root_d)}/problem.md)"
        elif r["oj_dir"] and os.path.exists(os.path.join(PSCP_ROOT, "oj", r["oj_dir"], "problem.md")):
            spec_link = f"[`problem.md`](oj/{url_quote(r['oj_dir'])}/problem.md)"
            
        sub_link = "-"
        if has_root_dir and os.path.exists(os.path.join(PSCP_ROOT, root_d, "submission.md")):
            sub_link = f"[`submission.md`]({url_quote(root_d)}/submission.md)"
                
        code_link = "-"
        if has_root_dir and os.path.exists(os.path.join(PSCP_ROOT, root_d, "main.py")):
            code_link = f"[`main.py`]({url_quote(root_d)}/main.py)"
        elif r["oj_dir"] and os.path.exists(os.path.join(PSCP_ROOT, "oj", r["oj_dir"], "main.py")):
            code_link = f"[`main.py`](oj/{url_quote(r['oj_dir'])}/main.py)"
            
        lines.append(f"| **{pid}** | {p_name} | Week {w} | {stat_badge} | {folder_link} | {spec_link} | {sub_link} | {code_link} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 4: Standard OJ Problems by Week
    lines.append("## 💻 4. Standard OJ Problems (จำแนกตามสัปดาห์ตั้งแต่เปิดเทอม)")
    lines.append("")

    for w in active_weeks:
        w_std_records = [r for r in records if r["week"] == w and not r["is_ll"]]
        if not w_std_records:
            continue
        w_pass_cnt = sum(1 for r in w_std_records if r["is_passed"])
        lines.append(f"### 📅 {WEEK_TITLES[w]}")
        lines.append("")
        lines.append(f"> รวม `{len(w_std_records)}` ข้อ (ผ่านแล้ว `{w_pass_cnt}/{len(w_std_records)}`)")
        lines.append("")
        lines.append("| OJ ID | Problem Name | Status | Folder Link | Problem Spec | Solution Code |")
        lines.append("| :---: | :--- | :---: | :--- | :---: | :---: |")
        for r in w_std_records:
            pid = r["id"]
            p_name = r["name"]
            stat_badge = "✅ **Passed**" if r["is_passed"] else "🔄 *In Progress*"
            
            folder_link = f"[`{r['oj_dir']}`](oj/{url_quote(r['oj_dir'])})" if r["oj_dir"] else "-"
            
            md_link = "-"
            if r["oj_dir"] and os.path.exists(os.path.join(PSCP_ROOT, "oj", r["oj_dir"], "problem.md")):
                md_link = f"[`problem.md`](oj/{url_quote(r['oj_dir'])}/problem.md)"
                
            code_link = "-"
            if r["oj_dir"] and os.path.exists(os.path.join(PSCP_ROOT, "oj", r["oj_dir"], "main.py")):
                code_link = f"[`main.py`](oj/{url_quote(r['oj_dir'])}/main.py)"
                
            lines.append(f"| **{pid}** | {p_name} | {stat_badge} | {folder_link} | {md_link} | {code_link} |")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Section 5: Data & Automation
    lines.append("## 🛠️ Data & Automation Scripts")
    lines.append("")
    lines.append(f"- [`oj_problems.json`](oj_problems.json) — Summary registry ({len(summary_list)} problems): id, week, status, pass stats, deadline, and category flags.")
    lines.append("- [`data/all_problems_detail.json`](data/all_problems_detail.json) — Detail registry: problem statements, input/output specifications, time/memory limits, and sample testcases.")
    lines.append(f"- `data/html_cache/` — Raw HTML snapshots of {html_cache_count} problem pages, kept locally for debugging the scraper (gitignored).")
    lines.append("- [`scripts/scrape_all_oj_problems.py`](scripts/scrape_all_oj_problems.py) — iJudge scraper: registries, `problem.md`, and `main.py` stubs, with a React Server Component (RSC) stream resolver.")
    lines.append("- [`scripts/submit_oj.py`](scripts/submit_oj.py) — Submission CLI with session-cookie management and result polling.")
    lines.append("- [`scripts/sync_oj_status.py`](scripts/sync_oj_status.py) — Renames `oj/` folders to match the pass status (✅ suffix).")
    lines.append("- [`scripts/update_readme.py`](scripts/update_readme.py) — Generates this README.md. Edit the script, not the README: manual edits are overwritten.")
    lines.append("- [`scripts/README.md`](scripts/README.md) — Setup, credentials, and every command option.")
    lines.append("")
    lines.append("### 🔁 Weekly Workflow")
    lines.append("")
    lines.append("```bash")
    lines.append("python3 scripts/scrape_all_oj_problems.py --fast          # refresh the problem list and status")
    lines.append("python3 scripts/scrape_all_oj_problems.py --only <ids>    # new problems -> problem.md + main.py stub")
    lines.append("python3 \"oj/oj<id>-<Name>/main.py\"                        # solve and test in VS Code")
    lines.append("python3 scripts/update_readme.py                          # regenerate this README")
    lines.append("```")
    lines.append("")
    if has_plan:
        lines.append("### 🗺️ Roadmap")
        lines.append("")
        lines.append("แผนจัดระเบียบ repo — registry เดียวเป็น JSON, เลิก ✅ ในชื่อโฟลเดอร์, แยกหน้าที่ branch, รวม scripts เป็น CLI เดียว — อยู่ที่ [`docs/PLAN.md`](docs/PLAN.md)")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🐍 Code Style Guidelines")
    lines.append("")
    lines.append("All Python solutions follow strict PEP-8 standards with docstrings:")
    lines.append("")
    lines.append("```python")
    lines.append('""" Problem Name """')
    lines.append("")
    lines.append("def main():")
    lines.append('    """Problem Name"""')
    lines.append("    # solution code here")
    lines.append("")
    lines.append('if __name__ == "__main__":')
    lines.append("    main()")
    lines.append("```")
    lines.append("")

    content = "\n".join(lines).strip() + "\n"
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully generated and wrote {README_PATH} ({len(lines)} lines)")

if __name__ == "__main__":
    generate_readme()
