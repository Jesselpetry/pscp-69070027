#!/usr/bin/env python3
"""
Scrape and format all PSCP OJ problems from iJudge.
Extracts:
1. Full HTML cache for every problem page
2. Complete structured JSON (problem description, input/output spec, notes, testcases, limits)
3. Formatted markdown (problem.md) for all problems matching the repository standard
4. User's saved/submitted code (beforeCode) if available
5. Fully resolves Next.js RSC binary byte streams & string references ($xx)
6. Organizes Learning Logs cleanly at root ojXXXX/ and standard/midterm in oj/
"""

import asyncio
import html
import json
import os
import re
import urllib.request
import websockets

PSCP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IHELP_ROOT = os.path.normpath(os.path.join(PSCP_ROOT, "..", "ihelp"))

HTML_CACHE_DIR_PSCP = os.path.join(PSCP_ROOT, "data", "html_cache")
HTML_CACHE_DIR_IHELP = os.path.join(IHELP_ROOT, "data", "html_cache")

JSON_OUT_PSCP = os.path.join(PSCP_ROOT, "data", "all_problems_detail.json")
JSON_OUT_IHELP = os.path.join(IHELP_ROOT, "data", "all_problems_detail.json")

OJ_PROBLEMS_PSCP = os.path.join(PSCP_ROOT, "oj_problems.json")
OJ_PROBLEMS_IHELP = os.path.join(IHELP_ROOT, "data", "oj_problems.json")

os.makedirs(HTML_CACHE_DIR_PSCP, exist_ok=True)
os.makedirs(HTML_CACHE_DIR_IHELP, exist_ok=True)
os.makedirs(os.path.dirname(JSON_OUT_PSCP), exist_ok=True)
os.makedirs(os.path.dirname(JSON_OUT_IHELP), exist_ok=True)

def clean_text(t):
    if not t:
        return ""
    # Normalize carriage returns
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    return t.strip()

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

async def scrape_all():
    res = urllib.request.urlopen("http://localhost:9222/json").read()
    targets = json.loads(res.decode("utf-8"))
    page = next((t for t in targets if t.get("type") == "page" and "ijudge" in t.get("url", "")), None)
    if not page:
        page = next(t for t in targets if t.get("type") == "page")
    ws_url = page["webSocketDebuggerUrl"]
    
    async with websockets.connect(ws_url) as ws:
        msg_id = 1
        async def send_eval(js):
            nonlocal msg_id
            msg_id += 1
            await ws.send(json.dumps({"id": msg_id, "method": "Runtime.evaluate", "params": {"expression": js, "awaitPromise": True, "returnByValue": True}}))
            while True:
                resp = json.loads(await ws.recv())
                if resp.get("id") == msg_id:
                    return resp.get("result", {}).get("result", {}).get("value")

        # Step 1: Collect all problem list from Course 78
        print("=== Step 1: Fetching Course 78 Problem List ===")
        all_problem_items = []
        for page_num in range(10):
            url = f"https://ijudge.it.kmitl.ac.th/courses/78/problems?page={page_num}"
            await ws.send(json.dumps({"id": 9000 + page_num, "method": "Page.navigate", "params": {"url": url}}))
            await asyncio.sleep(2.0)
            
            js_extract_list = """
            (() => {
                const table = document.querySelector('table');
                if (!table) return [];
                const rows = Array.from(table.querySelectorAll('tbody tr'));
                return rows.map(tr => {
                    const descLink = tr.querySelector('a[href*="/description"]');
                    if (!descLink) return null;
                    const href = descLink.href;
                    const matchId = href.match(/\\/problems\\/(\\d+)\\/description/);
                    const id = matchId ? parseInt(matchId[1]) : 0;
                    
                    const cells = Array.from(tr.children);
                    const statusCell = cells[0];
                    const svgHtml = statusCell ? statusCell.innerHTML : '';
                    const hasPassedIcon = svgHtml.includes('Check') || svgHtml.includes('green') || svgHtml.includes('M9 16.17');
                    
                    const diffCell = cells[2];
                    let difficulty = 0;
                    if (diffCell) {
                        const stars = diffCell.querySelectorAll('svg');
                        stars.forEach(s => {
                            if (s.outerHTML.includes('yellow') || s.outerHTML.includes('amber') || s.getAttribute('data-testid') === 'StarIcon') {
                                difficulty++;
                            }
                        });
                    }
                    
                    const passed_count = cells[3] ? parseInt(cells[3].innerText.trim()) || 0 : 0;
                    const attempt_count = cells[4] ? parseInt(cells[4].innerText.trim()) || 0 : 0;
                    const pctText = cells[5] ? cells[5].innerText.trim().replace('%', '') : '0';
                    const percentage = parseFloat(pctText) || 0.0;
                    const expire_date = cells[6] ? cells[6].innerText.trim() : '';

                    return {
                        id,
                        name: descLink.innerText.trim(),
                        status: hasPassedIcon ? "Passed" : (attempt_count > 0 ? "Not Passed" : "Not Submit"),
                        difficulty,
                        passed_count,
                        attempt_count,
                        percentage,
                        expire_date,
                        is_learning_log: descLink.innerText.includes("[LEARNING LOGS]") || descLink.innerText.includes("[LEARNING LOG]"),
                        is_recommended: descLink.innerText.toLowerCase().includes("[recommend"),
                        is_midterm: descLink.innerText.toUpperCase().includes("[ MIDTERM ]"),
                        url: href
                    };
                }).filter(Boolean);
            })()
            """
            items = await send_eval(js_extract_list)
            if not items:
                break
            print(f"  Page {page_num}: Found {len(items)} problems")
            for it in items:
                it["course_page"] = page_num
                all_problem_items.append(it)
                
        print(f"\nTotal course problems found: {len(all_problem_items)}")
        
        # Step 2: Scrape details, HTML cache, and RSC data for each problem
        print("\n=== Step 2: Scraping Problem Details & HTML Caches ===")
        all_problems_detail = []
        
        for idx, item in enumerate(all_problem_items, 1):
            pid = item["id"]
            p_name = item["name"]
            p_url = item["url"]
            c_page = item["course_page"]
            is_ll = item["is_learning_log"]
            is_rec = item["is_recommended"]
            is_passed = (item["status"] == "Passed")
            print(f"[{idx}/{len(all_problem_items)}] Processing OJ {pid}: {p_name} ...")
            
            # Fetch RSC
            js_rsc = f"""
            (async () => {{
                try {{
                    const res = await fetch('{p_url}', {{ headers: {{ 'RSC': '1' }} }});
                    return await res.text();
                }} catch (e) {{
                    return null;
                }}
            }})()
            """
            rsc_text = await send_eval(js_rsc)
            
            # Fetch full HTML
            js_html = f"""
            (async () => {{
                try {{
                    const res = await fetch('{p_url}');
                    return await res.text();
                }} catch (e) {{
                    return null;
                }}
            }})()
            """
            html_text = await send_eval(js_html)
            
            # Save HTML cache
            if html_text:
                with open(os.path.join(HTML_CACHE_DIR_PSCP, f"oj{pid}.html"), "w", encoding="utf-8") as f:
                    f.write(html_text)
                with open(os.path.join(HTML_CACHE_DIR_IHELP, f"oj{pid}.html"), "w", encoding="utf-8") as f:
                    f.write(html_text)

            # Parse stream chunks
            chunks = parse_rsc_stream(rsc_text) if rsc_text else {}
            full_combined = " ".join(chunks.values())

            prob_obj = parse_balanced_json(full_combined, "problem", "{", "}") if full_combined else None
            cp_obj = parse_balanced_json(full_combined, "courseProblem", "{", "}") if full_combined else None
            samples = parse_balanced_json(full_combined, "sampleCases", "[", "]") if full_combined else []
            submission = parse_balanced_json(full_combined, "submission", "{", "}") if full_combined else None
            before_code = extract_string_value(full_combined, "beforeCode") if full_combined else None
            
            # Resolve RSC references in prob_obj
            if prob_obj:
                for k in ["problem_description", "problem_input_specification", "problem_output_specification", "problem_note", "problem_title"]:
                    if k in prob_obj and isinstance(prob_obj[k], str):
                        prob_obj[k] = resolve_rsc_ref(prob_obj[k], chunks)
                        
            # Resolve RSC references in before_code
            if before_code and isinstance(before_code, str):
                before_code = resolve_rsc_ref(before_code, chunks)
            
            prob_detail = {
                "id": pid,
                "name": p_name,
                "status": item["status"],
                "difficulty": item["difficulty"],
                "passed_count": item["passed_count"],
                "attempt_count": item["attempt_count"],
                "percentage": item["percentage"],
                "expire_date": item["expire_date"],
                "is_learning_log": is_ll,
                "is_recommended": is_rec,
                "is_midterm": item.get("is_midterm", False),
                "url": p_url,
                "course_page": c_page,
                "courseProblem": cp_obj,
                "problem": prob_obj,
                "sampleCases": samples,
                "submission": submission,
                "beforeCode": before_code
            }
            all_problems_detail.append(prob_detail)
            
            # Format markdown
            problem_md_content = format_problem_markdown(prob_detail)
            
            # Save files according to repository conventions:
            # 1. Learning Logs: ONLY at root ojXXXX/
            if is_ll:
                ll_dir = os.path.join(PSCP_ROOT, f"oj{pid}")
                os.makedirs(ll_dir, exist_ok=True)
                with open(os.path.join(ll_dir, "problem.md"), "w", encoding="utf-8") as f:
                    f.write(problem_md_content)
                main_py_ll = os.path.join(ll_dir, "main.py")
                if not os.path.exists(main_py_ll) and before_code:
                    with open(main_py_ll, "w", encoding="utf-8") as f:
                        f.write(before_code)
                elif not os.path.exists(main_py_ll):
                    with open(main_py_ll, "w", encoding="utf-8") as f:
                        f.write(f'""" {p_name} """\n\n\ndef main():\n    """{p_name}"""\n    # solution code here\n\n\nif __name__ == "__main__":\n    main()\n')
                elif before_code:
                    with open(main_py_ll, "r", encoding="utf-8", errors="ignore") as f:
                        cur = f.read()
                    if "solution code here" in cur or len(cur.strip().splitlines()) <= 4:
                        with open(main_py_ll, "w", encoding="utf-8") as f:
                            f.write(before_code)

            # 2. Recommended problems in recommended/
            if is_rec:
                rec_folders = [d for d in os.listdir(os.path.join(PSCP_ROOT, "recommended")) if f"oj{pid}-" in d or d == f"oj{pid}"] if os.path.exists(os.path.join(PSCP_ROOT, "recommended")) else []
                if rec_folders:
                    p_md_path = os.path.join(PSCP_ROOT, "recommended", rec_folders[0], "problem.md")
                    with open(p_md_path, "w", encoding="utf-8") as f:
                        f.write(problem_md_content)

            # 3. Non-Learning-Logs in oj/
            if not is_ll:
                oj_folders = [d for d in os.listdir(os.path.join(PSCP_ROOT, "oj")) if f"oj{pid}-" in d or d == f"oj{pid}"] if os.path.exists(os.path.join(PSCP_ROOT, "oj")) else []
                if oj_folders:
                    target_dir_name = oj_folders[0]
                    # Update checkmark
                    clean_name = target_dir_name.replace(" ✅", "").strip()
                    desired_name = f"{clean_name} ✅" if is_passed else clean_name
                    if desired_name != target_dir_name:
                        os.rename(os.path.join(PSCP_ROOT, "oj", target_dir_name), os.path.join(PSCP_ROOT, "oj", desired_name))
                        target_dir_name = desired_name
                        
                    oj_dir_target = os.path.join(PSCP_ROOT, "oj", target_dir_name)
                    with open(os.path.join(oj_dir_target, "problem.md"), "w", encoding="utf-8") as f:
                        f.write(problem_md_content)
                    main_py_target = os.path.join(oj_dir_target, "main.py")
                    if os.path.exists(main_py_target):
                        with open(main_py_target, "r", encoding="utf-8", errors="ignore") as f:
                            cur_code = f.read()
                        if before_code and ("solution code here" in cur_code or len(cur_code.strip().splitlines()) <= 4):
                            with open(main_py_target, "w", encoding="utf-8") as f:
                                f.write(before_code)
                else:
                    safe_name = re.sub(r'[^\w\s-]', '', p_name).strip().replace(' ', '_')
                    folder_name = f"oj{pid}-{safe_name}"
                    if is_passed:
                        folder_name += " ✅"
                    oj_dir_target = os.path.join(PSCP_ROOT, "oj", folder_name)
                    os.makedirs(oj_dir_target, exist_ok=True)
                    with open(os.path.join(oj_dir_target, "problem.md"), "w", encoding="utf-8") as f:
                        f.write(problem_md_content)
                    main_py_path = os.path.join(oj_dir_target, "main.py")
                    if before_code:
                        with open(main_py_path, "w", encoding="utf-8") as f:
                            f.write(before_code)
                    else:
                        with open(main_py_path, "w", encoding="utf-8") as f:
                            f.write(f'""" {p_name} """\n\n\ndef main():\n    """{p_name}"""\n    # solution code here\n\n\nif __name__ == "__main__":\n    main()\n')

        # Step 3: Save Master JSONs
        print("\n=== Step 3: Saving Master Databases ===")
        with open(JSON_OUT_PSCP, "w", encoding="utf-8") as f:
            json.dump(all_problems_detail, f, indent=2, ensure_ascii=False)
        with open(JSON_OUT_IHELP, "w", encoding="utf-8") as f:
            json.dump(all_problems_detail, f, indent=2, ensure_ascii=False)
        print(f"Saved detailed JSON database ({len(all_problems_detail)} problems) to:")
        print(f"  - {JSON_OUT_PSCP}")
        print(f"  - {JSON_OUT_IHELP}")
        
        summary_list = []
        for p in all_problems_detail:
            summary_list.append({
                "id": p["id"],
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
            })
            
        with open(OJ_PROBLEMS_PSCP, "w", encoding="utf-8") as f:
            json.dump(summary_list, f, indent=2, ensure_ascii=False)
        with open(OJ_PROBLEMS_IHELP, "w", encoding="utf-8") as f:
            json.dump(summary_list, f, indent=2, ensure_ascii=False)
        print(f"Updated oj_problems.json in both repositories.")
        print("\n🎉 Complete scraping & synchronization finished successfully!")

if __name__ == "__main__":
    asyncio.run(scrape_all())
