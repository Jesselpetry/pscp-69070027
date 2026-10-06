# แผนจัดระเบียบ repo PSCP

> สถานะ: **ทำแล้วส่วนใหญ่** · ตัดสินใจ 2026-10-06 · รายการที่เหลืออยู่หัวข้อ 4

## 1. การตัดสินใจ

| # | เรื่อง | เลือก |
| :---: | :--- | :--- |
| D1 | public / private | คง repo เดียวแบบ **public** |
| D2 | branch | `main` = โจทย์ + โค้ดของตัวเอง · `OP` = scripts + data + คลังโค้ดครบ (`solutions/`) |
| D3 | ✅ ท้ายชื่อโฟลเดอร์ | **คงไว้** (script จัดการให้จากสถานะใน registry) |
| D4 | เลข week | **คงเลขเดิม** — คำนวณจากวันปล่อยโจทย์ + override 10 ข้อใน `data/course.json` |

## 2. โครงสร้างหลังจัด

```text
main  (root ของ repo — เขียนโค้ดที่นี่)
├── oj/oj<id>-<Name>[ ✅]/      problem.md (generated) + main.py
├── oj<id>/                     Learning Log: problem.md, main.py, submission.md
├── recommended/                เขียนเอง — script ไม่แตะ
├── README.md                   generated (pscp.py readme)
├── CONTRIBUTE.md
└── .op/                        worktree ของ OP (gitignored)

OP  (.op/)
├── data/
│   ├── course.json             ตั้งค่าเอง: week, tag หมวด, ชื่อโฟลเดอร์, course id, map midterm
│   ├── oj_problems.json        registry สรุป (มี released แล้ว)
│   ├── all_problems_detail.json
│   ├── course_84_problems.json
│   └── html_cache/             gitignored
├── solutions/oj<id>/main.py    คลังโค้ดที่ทำเสร็จ (key ด้วย id — ไม่ย้ายตาม ✅)
├── scripts/                    pscp.py + scripts + ijudge/ + tests/
└── docs/PLAN.md
```

กติกา:

1. **JSON เป็นต้นฉบับ** — `problem.md`, README, เลข week, ชื่อโฟลเดอร์ใหม่ ได้จาก `data/` ทั้งหมด
2. **ไฟล์ generate กับไฟล์เขียนเองไม่ปนกัน** — script เขียนทับได้แค่ `problem.md` ที่ generate และ README; ไม่แตะ `main.py` ที่มีโค้ดแล้ว, `submission.md`, `ai_reflection.md`, `recommended/`
3. **ไม่มีค่าตายตัวใน code** — ช่วง ID, ชื่อโฟลเดอร์, ชื่อหัวข้อ week, course id อยู่ใน `course.json`
4. **ไม่ merge ระหว่าง main กับ OP** — หน้าที่ไม่ทับกัน แต่ละ branch commit ของตัวเอง

## 3. ทำแล้ว

- [x] commit ผล scrape 6 ต.ค. (week 10–14) บน main และกู้ `recommended/*/problem.md` ที่ถูกเขียนทับ
- [x] สร้าง branch `OP` + worktree `.op/`; ย้าย `scripts/`, `data/`, `oj_problems.json` ออกจาก main
- [x] `solutions/` 134 ข้อ: โค้ดล่าสุดจาก main 131 ข้อ + 3355, 3357, 3360 จาก `solutions/2026-s1`
- [x] `data/course.json` แทน hardcode ทั้งหมด (week windows, override, 102 ชื่อโฟลเดอร์, tag หมวด, map course 84) — ตรวจแล้วเลข week ตรงของเดิมครบ 222 ข้อ
- [x] `ijudge/` ใหม่: `paths` (หา main/OP), `config` (course.json), `code` (template + ตรวจ stub ด้วย AST)
- [x] scripts: renderer แยกจาก scraper (แก้ HTML/`$`/tag ในโจทย์), README ไม่เขียน JSON แล้ว, `check_repo` (doctor), `archive_solutions`, `run_samples`, `pscp.py` CLI เดียว, tests
- [x] แก้ bug `IHELP_ROOT` ชี้ผิดที่ — เลิก mirror JSON; ihelp อ่านจาก `.op/` ตรง ๆ
- [x] README / CONTRIBUTE / scripts/README อัปเดตตามโครงสร้างใหม่

## 4. ที่เหลือ (ทำเองเมื่อพร้อม)

- [ ] ตรวจ branch `OP` แล้ว push: `git push -u origin OP` (และ `git push` บน main)
- [ ] ลบของเก่าเมื่อมั่นใจ: `git worktree remove .pscp-archive`, `git branch -D solutions/2026-s1`, `git push origin --delete solutions/2026-s1`
- [ ] ลบโฟลเดอร์ขยะ `Y1-S1/PSCP/ihelp/` (JSON 2 ไฟล์ที่ script เก่าเขียนผิดที่)
- [ ] ihelp: commit การแก้ `scripts/build_pscp_registry.py` / `verify_solutions.py` แล้ว rebuild (`bun run pscp:build`)
- [ ] เขียน `submission.md` ของ Learning Log ใหม่ (`check_repo` จะเตือนข้อที่ยังไม่มี)
- [ ] เมื่อมีสัปดาห์ใหม่: เพิ่ม 1 แถวใน `data/course.json` → `weeks` (ระวังเลข 14 ชนกับ Mini Exam — ย้าย Mini Exam ไปเลขอื่นใน `categories.mini_exam.week`)

## 5. Workflow ประจำสัปดาห์

```bash
python3 .op/scripts/pscp.py scrape --fast            # รายการโจทย์ + สถานะ
python3 .op/scripts/pscp.py scrape --only 3586-3598  # โจทย์ใหม่ → JSON → problem.md + main.py stub
# เขียนโค้ดใน oj/<folder>/main.py แล้วทดสอบใน VS Code
python3 .op/scripts/pscp.py test 3586                # รันกับ sample ทางการ
python3 .op/scripts/pscp.py status                   # ✅ ตามสถานะ iJudge
python3 .op/scripts/pscp.py archive                  # เก็บโค้ดที่เสร็จเข้า solutions/
python3 .op/scripts/pscp.py readme                   # README ใหม่
python3 .op/scripts/pscp.py doctor                   # ตรวจความสอดคล้อง
```
