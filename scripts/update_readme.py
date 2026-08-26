#!/usr/bin/env python3
"""
Generate and update README.md and oj_problems.json for pscp-69070027 and ihelp
with 100% complete metadata (recovered from git history and active iJudge scrape),
clickable problem tables, folder links, file links, status badges, and
proper chronological weekly grouping from Week 1 (เปิดเทอม) to Week 7 (Midterm).
"""

import json
import os
import re
import subprocess
import urllib.parse

PSCP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README_PATH = os.path.join(PSCP_ROOT, "README.md")
DETAIL_JSON = os.path.join(PSCP_ROOT, "data", "all_problems_detail.json")
OJ_PROBLEMS_PSCP = os.path.join(PSCP_ROOT, "oj_problems.json")

IHELP_ROOT = os.path.normpath(os.path.join(PSCP_ROOT, "..", "ihelp"))
OJ_PROBLEMS_IHELP = os.path.join(IHELP_ROOT, "data", "oj_problems.json")

def url_quote(path):
    return urllib.parse.quote(path)

def get_week(item):
    pid = item["id"]
    name = item.get("name", "")
    exp = item.get("expire_date", "")
    
    if item.get("is_midterm") or "[ MIDTERM ]" in name.upper() or (3274 <= pid <= 3282):
        return 7
    if "11 September" in exp or (3226 <= pid <= 3238):
        return 6
    if "4 September" in exp or pid in [3129, 3135] or (3155 <= pid <= 3167):
        return 5
    if "28 August" in exp or (3058 <= pid <= 3116):
        if pid <= 3072:
            return 3
        else:
            return 4
    if "14 August" in exp or "16 August" in exp or "17 August" in exp or (3020 <= pid <= 3042):
        return 2
    if "31 July" in exp or "7 August" in exp or pid <= 3019:
        return 1
    return 1

WEEK_TITLES = {
    1: "Week 1: บทนำ ตัวแปร และการรับส่งข้อมูลพื้นฐาน (Basic I/O & Variables)",
    2: "Week 2: การทำงานแบบมีเงื่อนไขพื้นฐาน (Basic Conditionals & Logic)",
    3: "Week 3: การทำงานแบบมีเงื่อนไขขั้นสูง (Nested Conditionals & Advanced Logic)",
    4: "Week 4: การทำงานซ้ำแบบ While Loop และตัวแปรสะสม (While Loops & Accumulators)",
    5: "Week 5: การทำงานซ้ำแบบ For Loop และลูปซ้อนลูป (For Loops & Geometry Drawing)",
    6: "Week 6: ลูปขั้นสูง สตริง และลำดับอนุกรม (Advanced Loops, Strings & Sequences)",
    7: "Week 7 / Midterm: ชุดข้อสอบจำลองกลางภาค (Midterm Mock Exam)"
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
                "url": p["url"]
            }

    # 3. Assign week
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
        week = meta.get("week") or get_week({"id": pid, "name": name, "expire_date": meta.get("expire_date", "")})
        
        records.append({
            "id": pid,
            "name": name,
            "week": week,
            "is_passed": is_passed,
            "is_rec": is_rec,
            "is_ll": is_ll,
            "is_midterm": is_mid,
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
    for w in range(1, 8):
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
    rec_records = [r for r in records if r["is_rec"]]
    ll_records = [r for r in records if r["is_ll"]]
    
    lines.append(f"| **🎯 Midterm Mock Exam** | {len(mid_records)} | {sum(1 for r in mid_records if r['is_passed'])} | {sum(1 for r in mid_records if not r['is_passed'])} |")
    lines.append(f"| **🌟 Recommended Problems** | {len(rec_records)} | {sum(1 for r in rec_records if r['is_passed'])} | {sum(1 for r in rec_records if not r['is_passed'])} |")
    lines.append(f"| **📓 Learning Logs** | {len(ll_records)} | {sum(1 for r in ll_records if r['is_passed'])} | {sum(1 for r in ll_records if not r['is_passed'])} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📁 Repository Structure")
    lines.append("")
    lines.append("```")
    lines.append("pscp-69070027/")
    lines.append("├── recommended/            # Curated Recommended Problems (10 problems with problem.md & solution)")
    lines.append("├── ojXXXX/                 # Learning Log folders ONLY (submission.md, main.py, problem.md)")
    lines.append("├── oj/                     # All Standard & Midterm OJ Problem folders")
    lines.append("├── data/")
    lines.append("│   ├── html_cache/         # Full offline HTML caches for all 67 course problems")
    lines.append("│   └── all_problems_detail.json # Master JSON database with testcases & specs")
    lines.append("├── scripts/                # Sync & scraping automation scripts")
    lines.append("└── AI-Guidelines-PSCP/     # Course AI instructions, policies, and templates")
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
    lines.append("## 🌟 2. Recommended Problems (คลังโจทย์แนะนำ 10 ข้อ)")
    lines.append("")
    lines.append("โจทย์สำคัญ 10 ข้อที่รวบรวมเทคนิคสำคัญของภาษา Python พร้อมคำอธิบายและแนวคิดอย่างละเอียด")
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

    for w in range(1, 7):
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
    lines.append("- [`data/all_problems_detail.json`](data/all_problems_detail.json) — Master JSON database containing complete problem statements, input/output specifications, time/memory limits, sample testcases, and week mappings.")
    lines.append("- [`data/html_cache/`](data/html_cache) — Offline HTML snapshots for all 67 course problems.")
    lines.append("- [`scripts/scrape_all_oj_problems.py`](scripts/scrape_all_oj_problems.py) — Automatic iJudge scraper & sync engine with React Server Component (RSC) binary byte-stream resolver.")
    lines.append("- [`scripts/sync_oj_status.py`](scripts/sync_oj_status.py) — Automatic folder status and checkmark tag synchronizer.")
    lines.append("- [`scripts/update_readme.py`](scripts/update_readme.py) — Auto-generates this README.md with real-time weekly progress and file links.")
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
