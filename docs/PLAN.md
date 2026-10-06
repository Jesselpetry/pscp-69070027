# แผนจัดระเบียบ repo PSCP

> สถานะ: **ร่าง — รอตัดสินใจ 4 ข้อในหัวข้อ 3** · ตรวจสภาพ repo เมื่อ 2026-10-06 · ยังไม่มีการย้ายไฟล์ใด ๆ

## 1. สรุปสั้น

- `main` ใหม่กว่า `solutions/2026-s1` แทบทุกอย่าง: หลังแยกกันที่ `62b3d95` (10 ก.ย.) main มี 13 commit ส่วน solutions มี 1 commit — main.py ต่างกัน 40 ข้อ: **37 ข้อ main ใหม่กว่า**, อีก 3 ข้อ (3355, 3357, 3360) มีโค้ดอยู่แค่ใน solutions
- `main` ไม่ได้เป็น branch "stub" อย่างที่ตั้งใจ: มีโค้ดแล้ว 131 จาก 222 ข้อ, เป็น stub 91 ข้อ (week 10–14 ที่เพิ่ง scrape + 3036, 3355, 3357, 3360)
- ข้อมูลโจทย์กระจายอยู่ใน JSON 3 ไฟล์ + ค่า hardcode ใน script อีก 6 จุด; ไฟล์โจทย์กระจาย 3 ที่ (`oj/`, `oj<id>/` ที่ root, `recommended/`)
- เป้าหมาย: **JSON ไฟล์เดียวเป็นต้นฉบับ** → generate `problem.md` และ README จากมัน · 1 โจทย์ = 1 โฟลเดอร์ที่ path ไม่เปลี่ยน · scripts เหลือ CLI เดียว · แต่ละ branch มีหน้าที่เดียว
- ข้อที่ต้องตัดสินใจก่อนสุด: repo นี้เป็น **public** แต่แนวทางของวิชาห้ามมี `main.py` และโจทย์ทางการใน public repo (หัวข้อ 2.5)

## 2. สภาพปัจจุบัน

### 2.1 Branch

| | `main` | `solutions/2026-s1` |
| :--- | :--- | :--- |
| commit ล่าสุด | `b8a77ea` · 25 ก.ย. 19:01 | `2f54a0d` · 24 ก.ย. 19:54 |
| นำอีกฝั่ง (นับจาก `62b3d95`) | 13 commit | 1 commit |
| ตรงกับ GitHub | ตรง | **local นำ origin 1 commit (ยังไม่ push)** |
| main.py ที่มีโค้ด | 131 | 134 |
| scripts | ใหม่กว่า | เก่า (`auth.py`, `client.py`, scraper, `submit_oj.py` ต่างกัน) |
| ของที่ยังไม่ commit | scrape วันที่ 6 ต.ค. (week 10–14, ~190 รายการ) | ไม่มี |

- 2 branch แยกทางกัน (diverged) — ไม่มีฝั่งไหนครอบคลุมอีกฝั่ง แต่ของที่มีเฉพาะใน solutions มีแค่โค้ด 3 ข้อข้างต้น
- commit `2f54a0d` ของ solutions (Week 8: 3294, 3295, 3297, 3300) มีเนื้อหาเดียวกับที่ main commit ไว้แล้ว
- ihelp build จาก worktree `.pscp-archive` (= solutions) จึงได้โค้ดเวอร์ชันเก่าของ 37 ข้อ

### 2.2 ข้อมูลโจทย์

| ไฟล์ | เนื้อหา | ปัญหา |
| :--- | :--- | :--- |
| `oj_problems.json` | สรุป 222 ข้อ (id, week, status, flag) | ซ้ำกับไฟล์ข้างล่าง, `update_readme.py` เขียนทับทุกครั้ง |
| `data/all_problems_detail.json` | ละเอียด 221 ข้อ (statement, sample, limit, `beforeCode`) | ขาด 2981, มีโค้ดที่ส่ง (`beforeCode`) ปนอยู่ |
| `data/course_84_problems.json` | โจทย์ Midterm ใน course 84 | การจับคู่กับ 3274–3282 hardcode อยู่ใน `submit_oj.py` |

โฟลเดอร์โจทย์:

- `oj/` 186 โฟลเดอร์ · `oj<id>/` ที่ root 36 โฟลเดอร์ (Learning Log) · `recommended/` 10 โฟลเดอร์ที่เป็น**สำเนา** — `main.py` ของ 2997, 2998, 3019, 3020, 3159 ไม่ตรงกับใน `oj/`
- ` ✅` ต่อท้ายชื่อโฟลเดอร์ทำให้ต้อง rename ทุกครั้งที่ผ่าน → git เห็นเป็นลบ + เพิ่ม (ตอนนี้ลบ 30 ไฟล์ + untracked อีกชุด), path มีช่องว่างและ emoji ต้อง quote ทุกครั้ง
- **scrape วันที่ 6 ต.ค. เขียนทับ `recommended/*/problem.md` ที่เขียนเอง 6 ไฟล์** (2996, 2997, 2998, 3019, 3020, 3022) — คำอธิบาย/เทคนิค/เทสเคสหายไป แทนด้วยโจทย์ดิบ ของเดิมยังอยู่ใน `HEAD` (ดู Phase 0)

### 2.3 สิ่งแปลกในโจทย์

- `problem.md` มี HTML ดิบ (`<br />`, `<b><u>`, `&nbsp;`) — ihelp มี `normalize_statement()` แก้เรื่องนี้แล้ว แต่ scraper ฝั่งนี้ไม่ได้ใช้
- `$` ในโจทย์ (เช่น 3362) ถูก GitHub แสดงเป็นสูตร LaTeX
- รูปในโจทย์ลิงก์ไป `ijudge.it.kmitl.ac.th:7159` — เปิดนอกระบบอาจไม่ขึ้น
- ชื่อโจทย์มี tag ปน และเขียนไม่สม่ำเสมอ: `[LEARNING LOGS]`, `[Recommend]`, `[ MIDTERM ]`, `[MINI EXAM]` กับ `[ MINI EXAM ]`, ช่องว่างเกิน (`Count All  Vowel`, `Tuple's Sad life `) — tag หลุดเข้าไปใน docstring ของ `main.py` ด้วย
- iJudge ลบ `[Recommend]` ออกจากชื่อหลังหมดเขต → `problem.md` เปลี่ยนเอง (3159, 3167)
- ชื่อแปลกจาก iJudge: `Day08-0_02-Backward`, `113`, `1132-Median`
- Mini Exam ซ้ำกัน 3 คู่: 3489/3507, 3490/3508, 3492/3509
- 2981 ไม่อยู่ในรายการของ iJudge แล้ว (มีแค่ใน `oj_problems.json`)
- week เดาจากช่วง ID + วันหมดเขต — แต่ตอนนี้แทบทุกข้อหมดเขต 25 ต.ค. แล้ว วันหมดเขตจึงใช้แยก week ไม่ได้; Mini Exam ถูกนับเป็น "Week 14" ทั้งที่ไม่ใช่สัปดาห์
- ข้อมูลที่ใช้แยก week ได้จริงคือ `courseProblem.cp_release_time` (วันปล่อยโจทย์): 14 รอบ ทุกวันศุกร์ ตรงกับ lab แต่ละสัปดาห์

### 2.4 Scripts

| ปัญหา | อยู่ที่ |
| :--- | :--- |
| ช่วง ID ของ week / midterm / mini exam hardcode ซ้ำ 3 ที่ | `ijudge/weeks.py`, `ijudge/course.py`, `update_readme.py` |
| ชื่อโฟลเดอร์ 38 ข้อ hardcode (`FOLDER_ALIASES`) | `scrape_all_oj_problems.py` |
| รายการข้อที่ผ่าน 32 ข้อ hardcode (`EARLIER_PASSED_PIDS`) | `sync_oj_status.py` |
| `MIDTERM_ALIAS_MAP`, server action id, course 78/84, `WEEK_TITLES` hardcode | `submit_oj.py`, `ijudge/auth.py`, `update_readme.py` |
| `IHELP_ROOT` ชี้ผิด: `PSCP/ihelp` แทน `IT-KMITL/ihelp` → เขียน JSON ลงโฟลเดอร์ขยะ `Y1-S1/PSCP/ihelp/` และ `ihelp/data/` ค้างที่ 10 ก.ย. | `scrape_all_oj_problems.py`, `update_readme.py` |
| `update_readme.py` เขียน `oj_problems.json` ด้วย (2 repo), ขุด git history หา stat, ไม่มี `--dry-run`, ตัดสินว่าผ่านจากคำว่า "Pass" ใน `submission.md` | `update_readme.py` |
| scraper เขียนทับไฟล์ที่เขียนเอง | `scrape_all_oj_problems.py` (ส่วน `recommended/`) |
| หาไฟล์โค้ดด้วย glob 5 ชั้น จนถึง `**/*<id>*.py` — หยิบผิดไฟล์ได้ | `submit_oj.find_solution_file` |
| ตัวหา cookie เขียนซ้ำกับ `ijudge.auth.resolve_cookie` | `submit_oj.find_cookie` |
| logic rename ✅ ซ้ำกับใน scraper | `sync_oj_status.py` |
| ฟังก์ชันไม่ถูกใช้ (`_retry_after`), `import requests` ในลูป, ไม่มี `requirements.txt`, ไม่มี test | `ijudge/client.py`, ทั้งโฟลเดอร์ |

### 2.5 ความเสี่ยง

- `github.com/Jesselpetry/pscp-69070027` เป็น **public** และ push ทั้ง 2 branch แล้ว
- แนวทางวิชา (`AI-Guidelines-PSCP/README.th.md` หัวข้อ 13–14): public repo ใช้เก็บ learning log เท่านั้น — **ห้ามมี** official OJ problem statements, official solutions และไฟล์ source เต็มอย่าง `main.py` (folder learning log ก็ห้ามมี `main.py`)
- ตอนนี้ repo มีครบทุกอย่างที่ห้าม: `problem.md` ทุกข้อ, `all_problems_detail.json` (โจทย์ + sample + โค้ดที่ส่ง), `main.py` ทุกข้อ, branch solutions
- ihelp (public เช่นกัน) commit `data/pscp/problems.json` ที่มี `referenceCode` และโจทย์ — หน้าเว็บตัดโค้ดออกแล้ว แต่ไฟล์ใน GitHub ยังมี
- commit `2fa0b71` มี `submit_config.json` ที่มี `access_token` อยู่ใน history (อายุ token ~24 ชม. น่าจะหมดแล้ว)

## 3. ตัดสินใจก่อนเริ่ม

| # | เรื่อง | ตัวเลือก | แนะนำ |
| :---: | :--- | :--- | :--- |
| D1 | public / private | **A** คง repo เดียวแบบ public (ยังเสี่ยงตาม 2.5) · **B** เปลี่ยน repo นี้เป็น private + rename เป็น `pscp-workspace` แล้วสร้าง `pscp-69070027` ใหม่ (public) ที่มีแค่ README + `oj<id>/submission.md` | **B** — ไม่ต้องเขียน history ใหม่, URL เดิมกลายเป็นของ repo ใหม่, fork = 0 |
| D2 | branch solutions | **A** แบบเดิม: ทั้ง tree (ต้อง merge scripts/data ข้ามไปมา → drift แบบตอนนี้) · **B** orphan branch ที่เก็บแค่ `oj/*/main.py` เป็นคลังโค้ด | **B** — scripts/data อยู่บน main ที่เดียว ไม่ต้อง merge อีก |
| D3 | ✅ ในชื่อโฟลเดอร์ | **A** คงไว้ · **B** เลิก — สถานะอยู่ใน JSON และ README | **B** — path คงที่, ไม่มี rename churn |
| D4 | การนับ week | **A** ตามวันปล่อยโจทย์: week 1–7 ก่อน midterm, Midterm/Mini Exam เป็นหมวด ไม่ใช่ week, week 8–13 หลัง midterm (เลขเดิม) — ข้อก่อน midterm 82 ข้อเลขขยับ (+1 เป็นส่วนใหญ่) · **B** คงเลขเดิมผ่านตาราง override | **A** — คำนวณได้จากข้อมูล ไม่ต้องดูแลช่วง ID |

ถ้าเลือก D1 = B: อาจารย์อาจดูวันที่ commit ของ `submission.md` — ให้สร้าง public repo ใหม่จาก clone ที่กรองด้วย `git filter-repo --path-glob 'oj[0-9]*/submission.md' --path-glob 'oj[0-9]*/ai_reflection.md'` วันที่ commit เดิมจะยังอยู่

## 4. โครงสร้างเป้าหมาย

### 4.1 หลักการ

1. **JSON เป็นต้นฉบับเดียว** — `problem.md`, README, รายการ week สร้างจาก JSON ทั้งหมด
2. **ไฟล์ generate กับไฟล์เขียนเองไม่ปนกัน** — script เขียนทับได้แค่ไฟล์ generate (`problem.md`, README); ไฟล์เขียนเอง (`main.py` หลังสร้าง, `notes.md`, `submission.md`, `ai_reflection.md`, `data/course.json`) script ไม่แตะ
3. **path ไม่เปลี่ยนตามสถานะ** — ไม่มี ✅ ในชื่อ ไม่ rename ตอนผ่าน
4. **1 โจทย์ = 1 โฟลเดอร์** — เลิกสำเนาใน `recommended/` (recommended เป็นแค่ flag); โค้ด Learning Log ย้ายมาอยู่ `oj/` เหมือนข้ออื่น, `oj<id>/` ที่ root เหลือแค่ learning log ตามแบบของวิชา

### 4.2 Workspace (repo นี้ — private ถ้า D1 = B)

```text
pscp-workspace/
├── README.md                    # generated: progress + ตารางโจทย์
├── data/
│   ├── course.json              # เขียนเอง: course id, ตาราง week, ชื่อโฟลเดอร์ที่ตั้งเอง
│   ├── problems.json            # generated: registry เดียว แทน oj_problems.json + all_problems_detail.json
│   └── cache/                   # gitignored: HTML/RSC ดิบ, beforeCode
├── oj/
│   └── oj3381-Point_Sorting/
│       ├── problem.md           # generated จาก problems.json — ห้ามแก้มือ
│       ├── main.py              # stub → โค้ดของเรา (script สร้างครั้งเดียว ไม่เขียนทับ)
│       └── notes.md             # มีหรือไม่มีก็ได้ เขียนเอง
├── oj3381/                      # learning log ตามแบบวิชา
│   ├── submission.md
│   └── ai_reflection.md         # เฉพาะเมื่อใช้ AI
├── scripts/                     # ดูหัวข้อ 5
├── docs/
│   ├── PLAN.md
│   ├── CONTRIBUTE.md            # ย้ายจาก root + เขียนใหม่ตามโครงสร้างนี้
│   └── notes/ce-kmitl/          # ย้ายจาก recommended/ce-kmitl/
├── AI-Guidelines-PSCP/
└── .pscp-archive/               # gitignored: worktree ของ branch solutions
```

ถ้า D1 = B, `oj<id>/` (learning log) จะอยู่ใน public repo แทน และ workspace เก็บต้นร่างไว้ที่เดียวกันแล้ว copy ไปด้วยคำสั่ง `publish-logs`

### 4.3 Public repo (เฉพาะ D1 = B)

```text
pscp-69070027/
├── README.md                    # ตาราง learning log + ลิงก์ submission.md
├── oj3227/
│   └── submission.md
├── oj3232/
│   ├── submission.md
│   └── ai_reflection.md
└── .gitignore                   # ตามแนวทางวิชา: *_work/, main.py, __pycache__/, .env, .DS_Store
```

### 4.4 `data/problems.json` (ร่าง)

```json
{
  "id": 3381,
  "folder": "oj3381-Point_Sorting",
  "title": "Point Sorting",
  "raw_title": "[LEARNING LOGS] Point Sorting",
  "week": 10,
  "category": "lab",
  "learning_log": true,
  "recommended": false,
  "released": "2026-09-11",
  "deadline": "2026-10-16T23:59",
  "status": "not_submitted",
  "stats": {"passed": 0, "attempted": 0},
  "limits": {"time_s": 1, "memory_kb": 32000},
  "statement": {"description": "...", "input": "...", "output": "...", "note": "..."},
  "samples": [{"input": "...", "output": "..."}],
  "ijudge": {"course_id": 78, "cp_id": 3381, "problem_id": 0, "url": "https://ijudge.it.kmitl.ac.th/problems/3381/description"}
}
```

- `category`: `lab` | `midterm` | `mini_exam` · `status`: `passed` | `attempted` | `not_submitted`
- `title` ตัด tag ออกแล้ว, `statement` แปลง HTML เป็น markdown แล้ว (escape `$`)
- `beforeCode` ไม่อยู่ใน registry — เก็บใน `data/cache/` (gitignored)

### 4.5 `data/course.json` (ร่าง)

```json
{
  "semester": "2026-S1",
  "courses": {"lab": 78, "midterm": 84},
  "weeks": [
    {"week": 1, "released": "2026-07-03", "title": "..."},
    {"week": 2, "released": "2026-07-10", "title": "..."}
  ],
  "categories": {
    "midterm": {"released": "2026-08-17", "title_tag": "MIDTERM"},
    "mini_exam": {"title_tag": "MINI EXAM"}
  },
  "folders": {"3290": "Left_Arrow", "3227": "Cards_44"},
  "midterm_map": {"3243": 3282}
}
```

- `weeks` แทน `get_week()` ทั้งหมด — โจทย์ใหม่ก็แค่เพิ่ม 1 บรรทัด
- `folders` แทน `FOLDER_ALIASES` — ชื่อโจทย์ภาษาไทยต้องตั้งเอง ถ้าไม่ตั้งใช้ `oj<id>` เฉย ๆ
- `midterm_map` แทน `MIDTERM_ALIAS_MAP` และ `data/course_84_problems.json`
- ชื่อหัวข้อ week ย้ายจาก `WEEK_TITLES` แล้วตรวจใหม่ เพราะเลข week ก่อน midterm เลื่อน (ถ้า D4 = A)

## 5. Scripts เป้าหมาย

```text
scripts/
├── pscp.py              # CLI เดียว: python3 scripts/pscp.py <คำสั่ง>
├── ijudge/              # คุยกับ iJudge เท่านั้น: auth, client, rsc parser, submit API
├── repo/                # ของในเครื่อง: config, registry, paths, render, stub, normalize
├── tests/               # week, ชื่อโฟลเดอร์, normalize, rsc parser
└── requirements.txt     # requests
```

| คำสั่ง | ทำอะไร | แทนของเดิม |
| :--- | :--- | :--- |
| `fetch [--only IDS] [--fast]` | iJudge → `data/problems.json` (+ cache) ไม่แตะโฟลเดอร์โจทย์ | ครึ่งแรกของ `scrape_all_oj_problems.py` |
| `render` | `problems.json` → `problem.md` ทุกข้อ + สร้าง `main.py` stub ที่ยังไม่มี (ไม่ต่อเน็ต รันซ้ำกี่ครั้งก็ได้ผลเดิม) | ครึ่งหลังของ scraper |
| `readme` | สร้าง README อย่างเดียว ไม่เขียน JSON | `update_readme.py` |
| `status` | สรุปต่อ week: stub / มีโค้ด / ผ่าน | `sync_oj_status.py` |
| `doctor` | ตรวจความสอดคล้อง: registry ↔ โฟลเดอร์, โฟลเดอร์ซ้ำ, learning log ขาด `submission.md`, `problem.md` ไม่ตรง JSON | ใหม่ |
| `test <id>` | รัน `main.py` กับ sample ใน JSON | `ihelp/scripts/verify_solutions.py` |
| `archive <id>` / `restore <id>` / `blank <id>` | เก็บโค้ดเข้า branch solutions / ดึงกลับ / ล้างเป็น stub | ทำมือ |
| `publish-logs` | copy learning log ไป public repo (D1 = B) | ใหม่ |
| `submit ...` | เหมือนเดิม แต่หาไฟล์จาก registry และใช้ `ijudge.auth` | `submit_oj.py` |

กติกา:

- ทุกคำสั่งที่เขียนไฟล์มี `--dry-run` ผ่าน `ijudge/fsio.py` ที่มีอยู่แล้ว
- เลิก mirror JSON ไป ihelp — ihelp อ่านจาก workspace ตรง ๆ (`PSCP_ARCHIVE_REPO` มีอยู่แล้วใน `build_pscp_registry.py`)
- ไม่มีช่วง ID ใน code อีก — ทุกอย่างอยู่ใน `course.json`

## 6. ขั้นตอน

ทำทีละ phase, 1 phase = 1 commit (หรือ 1 PR) ตรวจด้วย `doctor` ก่อนไป phase ถัดไป

### Phase 0 — เคลียร์ของค้าง (ยังไม่ย้ายไฟล์)

- [ ] ตัดสินใจ D1–D4
- [ ] กู้ `recommended/*/problem.md` ที่ถูกเขียนทับ:
  `git restore recommended/oj2996-Swap_Characters/problem.md recommended/oj2997-Elo/problem.md recommended/oj2998-EuclideanDistance2D/problem.md recommended/oj3019-Safe_Password/problem.md recommended/oj3020-Coke/problem.md recommended/oj3022-Temperature/problem.md`
- [ ] commit ผล scrape 6 ต.ค. บน main (หลังกู้ข้อบน)
- [ ] commit `2f54a0d` บน solutions: push หรือทิ้งก็ได้ (เนื้อหาซ้ำกับ main)
- [ ] ลบโฟลเดอร์ขยะ `Y1-S1/PSCP/ihelp/` (มีแค่ JSON 2 ไฟล์ที่ script เขียนผิดที่)
- [ ] D1 = B: GitHub → Settings → Change visibility → Private → Rename เป็น `pscp-workspace` แล้ว `git remote set-url origin https://github.com/Jesselpetry/pscp-workspace.git`

### Phase 1 — รวมข้อมูลเป็น JSON

- [ ] เขียน `data/course.json` (week จากวันปล่อย, ชื่อหัวข้อ, `folders` จาก `FOLDER_ALIASES` + ชื่อโฟลเดอร์ปัจจุบัน, `midterm_map`)
- [ ] script migrate ครั้งเดียว: `oj_problems.json` + `all_problems_detail.json` → `data/problems.json`
- [ ] เพิ่ม 2981 เอง (ไม่อยู่ใน iJudge แล้ว)
- [ ] ย้าย `beforeCode` ไป `data/cache/`
- [ ] ระหว่างรอ Phase 5: generate `oj_problems.json` จาก `problems.json` ไว้ให้ ihelp/submit ใช้ต่อ

### Phase 2 — ย้ายโฟลเดอร์ (`git mv` ทั้งหมดใน commit เดียว)

- [ ] `oj/<ชื่อ> ✅` → `oj/<folder>` (เอา ✅ ออก)
- [ ] Learning Log: `oj<id>/main.py` + `problem.md` → `oj/<folder>/`; `oj<id>/` เหลือ `submission.md` (+ `ai_reflection.md`)
- [ ] `recommended/<x>/problem.md` (ฉบับที่เขียนเอง) → `oj/<folder>/notes.md`
- [ ] `main.py` ใน `recommended/` ที่ต่างจาก `oj/` (2997, 2998, 3019, 3020, 3159): เลือกเก็บฉบับเดียว แล้วลบ `recommended/`
- [ ] `recommended/ce-kmitl/` → `docs/notes/ce-kmitl/`
- [ ] `render` → `problem.md` ใหม่ทุกข้อ (HTML สะอาด, ชื่อไม่มี tag)
- [ ] `CONTRIBUTE.md` → `docs/` + เขียนใหม่ (ไม่มี ✅, กฎ learning log ตามวิชา)

### Phase 3 — Scripts

- [ ] แยก `ijudge/` (network) กับ `repo/` (local)
- [ ] `pscp.py` + คำสั่งตามหัวข้อ 5; ลบ `scrape_all_oj_problems.py`, `update_readme.py`, `sync_oj_status.py`
- [ ] week จาก `cp_release_time` + `course.json`; ลบช่วง ID ทั้งหมด
- [ ] ย้าย `normalize_statement()` จาก ihelp มาเป็น lib กลาง
- [ ] README = template + ส่วน generate, ไม่เขียน JSON
- [ ] `requirements.txt`, `pyproject.toml` (pylint/ruff), `tests/`

### Phase 4 — Branch

- [ ] D2 = B: สร้าง orphan `solutions` จากโค้ดล่าสุดของ main (131 ข้อ) + 3355, 3357, 3360 จาก `solutions/2026-s1` → มีแค่ `oj/<folder>/main.py`
- [ ] tag ของเก่าไว้ก่อนลบ: `git tag archive/solutions-2026-s1 solutions/2026-s1`
- [ ] `git worktree remove .pscp-archive` → `git worktree add .pscp-archive solutions`
- [ ] main: `blank` ข้อที่อยากฝึกใหม่ (โค้ดยังอยู่ใน solutions)
- [ ] D1 = B: สร้าง public `pscp-69070027` ใหม่ (filter-repo ตามหัวข้อ 3) + README + `.gitignore` ของวิชา
- [ ] **ต้องทำพร้อม Phase 5 ข้อแรก** — ihelp อ่าน `oj_problems.json` จาก `.pscp-archive` ซึ่งจะไม่มีแล้ว ถ้าไม่แก้ `bun run pscp:build` จะพัง

### Phase 5 — ihelp + เอกสาร

- [ ] ihelp `build_pscp_registry.py` / `verify_solutions.py`: อ่าน `data/problems.json` จาก workspace + โค้ดจาก `.pscp-archive/oj/*/main.py` แทนการ scan โฟลเดอร์
- [ ] ihelp: เลิก commit `referenceCode` ลง repo (สร้างตอน build) ถ้าไม่อยากให้เฉลยอยู่บน GitHub
- [ ] อัปเดต README, `scripts/README.md`, `docs/CONTRIBUTE.md` ให้ตรงของจริง

## 7. Workflow ประจำสัปดาห์ (หลังจัดเสร็จ)

```bash
python3 scripts/pscp.py fetch            # โจทย์ใหม่ + สถานะ → data/problems.json
python3 scripts/pscp.py render           # problem.md + main.py stub
# ทำโจทย์ใน oj/<folder>/main.py แล้วทดสอบใน VS Code
python3 scripts/pscp.py test 3381        # รันกับ sample ทางการ
python3 scripts/pscp.py archive 3381     # เก็บโค้ดเข้า branch solutions
python3 scripts/pscp.py readme           # อัปเดต README
python3 scripts/pscp.py doctor           # ตรวจว่าไม่มีอะไรหลุด
```
