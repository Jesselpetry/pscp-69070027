#!/usr/bin/env python3
"""
Sync OJ Problems from iJudge to pscp-69070027 and ihelp repos.
Prerequisite: Google Chrome open at iJudge (https://ijudge.it.kmitl.ac.th) with remote debugging enabled or active.
"""

import asyncio
import json
import os
import urllib.request
import websockets

PSCP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IHELP_ROOT = os.path.normpath(os.path.join(PSCP_ROOT, "..", "ihelp"))

PSCP_JSON = os.path.join(PSCP_ROOT, "oj_problems.json")
IHELP_JSON = os.path.join(IHELP_ROOT, "data", "oj_problems.json")

async def eval_js_on_page(page_num):
    res = urllib.request.urlopen("http://localhost:9222/json").read()
    targets = json.loads(res.decode('utf-8'))
    target = next((t for t in targets if t.get('type') == 'page' and 'ijudge' in t.get('url', '')), None)
    if not target:
        raise Exception("No iJudge page found in CDP targets. Please ensure Chrome is open at iJudge.")
        
    ws_url = target['webSocketDebuggerUrl']
    async with websockets.connect(ws_url) as ws:
        url = f"https://ijudge.it.kmitl.ac.th/courses/78/problems?page={page_num}"
        await ws.send(json.dumps({"id": 1, "method": "Page.navigate", "params": {"url": url}}))
        await ws.recv()
        await asyncio.sleep(2.0)
        
        js_code = """
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
                const name = descLink.innerText.trim();
                
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
                    name,
                    status: hasPassedIcon ? "Passed" : (attempt_count > 0 ? "Not Passed" : "Not Submit"),
                    difficulty,
                    passed_count,
                    attempt_count,
                    percentage,
                    expire_date,
                    is_learning_log: name.includes("[LEARNING LOGS]"),
                    url: href
                };
            }).filter(Boolean);
        })()
        """
        eval_req = {"id": 2, "method": "Runtime.evaluate", "params": {"expression": js_code, "returnByValue": True}}
        await ws.send(json.dumps(eval_req))
        resp = await ws.recv()
        val = json.loads(resp).get("result", {}).get("result", {}).get("value", [])
        return val

def main():
    existing_ids = set()
    if os.path.exists(PSCP_JSON):
        with open(PSCP_JSON, "r", encoding="utf-8") as f:
            old_data = json.load(f)
            existing_ids = {p['id'] for p in old_data}
            
    print(f"Existing problem count before sync: {len(existing_ids)}")
    
    all_problems = {}
    page_num = 0
    empty_count = 0
    
    while page_num < 15:
        print(f"Fetching page {page_num}...")
        try:
            items = asyncio.run(eval_js_on_page(page_num))
            if not items:
                print(f"Page {page_num} returned 0 items.")
                empty_count += 1
                if empty_count >= 2:
                    print(f"Reached end of pages at page {page_num}.")
                    break
            else:
                empty_count = 0
                print(f"Page {page_num}: Extracted {len(items)} problems")
                for p in items:
                    all_problems[p['id']] = p
        except Exception as e:
            print(f"Error on page {page_num}: {e}")
            break
        page_num += 1
        
    sorted_problems = sorted(all_problems.values(), key=lambda x: x['id'])
    print(f"Total fetched problems: {len(sorted_problems)}")
    
    new_problems = [p for p in sorted_problems if p['id'] not in existing_ids]
    print(f"\nNewly added problems ({len(new_problems)}):")
    for np in new_problems:
        print(f"  - OJ {np['id']}: {np['name']} | Expire: {np['expire_date']} | LearningLog: {np['is_learning_log']}")
        
    # Save to pscp-69070027
    if os.path.exists(os.path.dirname(PSCP_JSON)):
        with open(PSCP_JSON, "w", encoding="utf-8") as f:
            json.dump(sorted_problems, f, ensure_ascii=False, indent=2)
        print(f"\nUpdated {PSCP_JSON}")

    # Save to ihelp
    if os.path.exists(os.path.dirname(IHELP_JSON)):
        with open(IHELP_JSON, "w", encoding="utf-8") as f:
            json.dump(sorted_problems, f, ensure_ascii=False, indent=2)
        print(f"Updated {IHELP_JSON}")

if __name__ == "__main__":
    main()
