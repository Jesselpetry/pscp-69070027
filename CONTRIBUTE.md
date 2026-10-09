# CONTRIBUTE.md — คู่มือเพิ่มและทำโจทย์ PSCP แบบ Fast-Track

เอกสารนี้รวบรวม **ขั้นตอนการทำงานมาตรฐาน (Standard Workflow)** สำหรับการเพิ่มโจทย์ใหม่, เขียนโค้ด, ตรวจสอบ, ส่งตรวจ iJudge, ซิงค์ระบบ และ commit อย่างรวดเร็วและถูกต้อง 100%

---

## ⚡ Fast-Track Pipeline (ขั้นตอนด่วนเมื่อได้รับโจทย์ใหม่)

เมื่อได้รับโจทย์ใหม่ (เช่น ลิงก์ iJudge, เลข OJ ID, หรือชื่อโจทย์) ให้ดำเนินการตาม 8 ขั้นตอนนี้ตามลำดับ:

```
[1. Check Auth] ──> [2. Config Course] ──> [3. Scrape & Render] ──> [4. Solve Code]
                                                                            │
[8. Commit & Push] <── [7. Post-Pass Sync] <── [6. Submit iJudge] <── [5. Test Samples]
```

### 1. ตรวจสอบ Session Cookie (iJudge Auth)
เครื่องมือใน repo มีระบบ **Auto-Refresh** จากโปรไฟล์ของ Zen Browser (`cookies.sqlite`) โดยอัตโนมัติ  
แต่หากต้องการตั้งค่าด้วยตนเองหรือ session หมดอายุ:
```bash
# ตรวจสอบว่า cookie ใช้งานได้หรือไม่ (แสดงชื่อผู้ใช้และคอร์ส)
python3 .op/scripts/pscp.py submit --dry-run --ids 3599
```
*หากต้องการดึง Cookie จาก Zen Browser แบบด่วน (One-Liner):*
```bash
python3 -c "import sqlite3, shutil, os, json, glob; p = glob.glob(os.path.expanduser('~/Library/Application Support/zen/Profiles/*.Default*/cookies.sqlite'))[0]; shutil.copy2(p, '/tmp/z.sqlite'); c = sqlite3.connect('/tmp/z.sqlite').cursor(); t = c.execute(\"SELECT value FROM moz_cookies WHERE host LIKE '%ijudge%' AND name='access_token'\").fetchone(); os.remove('/tmp/z.sqlite'); conf = json.load(open('.op/submit_config.json')); conf['cookie'] = f'access_token={t[0]}'; json.dump(conf, open('.op/submit_config.json', 'w'), indent=2); print('Cookie refreshed!')"
```

---

### 2. ตรวจสอบ Config ของโจทย์ใน `.op/data/course.json` (ก่อนดึงโจทย์)
หากโจทย์เข้าเงื่อนไขต่อไปนี้ ให้เพิ่มค่าใน [`.op/data/course.json`](file:///.op/data/course.json) ก่อน:
1. **โจทย์ชื่อภาษาไทย**: ให้เพิ่มการแปลงเป็นภาษาอังกฤษใน `"folder_names"` เพื่อไม่ให้ชื่อโฟลเดอร์กลายเป็น `oj<id>` เปล่าๆ:
   ```json
   "folder_names": {
     "3600": "Calories"
   }
   ```
2. **ขึ้นสัปดาห์ใหม่**: หากโจทย์ถูกปล่อยในสัปดาห์ใหม่ ให้เช็คว่าใน `"weeks"` มี `"from": "YYYY-MM-DD"` ระบุวันที่เริ่มสัปดาห์นั้นแล้ว:
   ```json
   {"week": 14, "from": "2026-10-09", "title": "ชุดข้อสอบย่อยจำลอง (Mini Exam / Mock Test)"}
   ```

---

### 3. ดึงโจทย์และสร้างโครงไฟล์ (Scrape & Render)
ดึงรายละเอียดของโจทย์จาก iJudge พร้อมสร้างโฟลเดอร์, `problem.md`, และ stub ของ `main.py`:
```bash
# ดึงเฉพาะข้อที่ต้องการ (ระบุ id เดี่ยว หรือช่วง เช่น 3599,3600 หรือ 3586-3598)
python3 .op/scripts/pscp.py scrape --only <ids>
```
*สิ่งที่ระบบสร้างให้:*
- `oj/oj<id>-<Problem_Name>/problem.md`: รายละเอียดโจทย์, Input/Output spec, ข้อจำกัดเวลา/หน่วยความจำ, และ Sample cases
- `oj/oj<id>-<Problem_Name>/main.py`: โครงไฟล์ stub พร้อม docstring มาตรฐาน

---

### 4. เขียนโค้ดเฉลย (Solve Problem)
เปิดไฟล์ `oj/oj<id>-<Problem_Name>/main.py` แล้วเขียนตรรกะโปรแกรม  
**กฎเหล็กของโครงสร้างโค้ดและ PEP 8 (เพื่อให้ได้คะแนน 10.0 เต็ม):**
```python
""" Problem Name """


def main():
    """Problem Name"""
    # โค้ดแก้ปัญหาที่นี่


if __name__ == "__main__":
    main()
```
- ✅ มี Module docstring บรรทัดแรกสุด
- ✅ โค้ดทั้งหมดอยู่ใน `def main():` และมี docstring บรรทัดแรกในฟังก์ชัน
- ✅ เว้น 2 บรรทัดว่างระหว่าง `def main():` กับ `if __name__ == "__main__":`
- ✅ ความยาวแต่ละบรรทัดห้ามเกิน 79 ตัวอักษร
- ✅ ห้ามมี Trailing whitespace ท้ายบรรทัด
- ✅ ไม่มี Unused imports หรือตัวแปรที่ไม่ได้ใช้

---

### 5. ทดสอบกับตัวอย่างและตรวจ Lint (Test & Lint)
ทดสอบโค้ดกับ Official Sample Cases จาก iJudge และตรวจ PEP 8:
```bash
# 1. รัน Sample testcases
python3 .op/scripts/pscp.py test <id>

# 2. ตรวจ PEP 8 Linting
flake8 "oj/oj<id>-<Problem_Name>/main.py"
```
*ต้องผ่านทุก sample testcase (`PASS`) และไม่มี flake8 warning ใดๆ ก่อนส่ง*

---

### 6. ส่งตรวจเข้า iJudge (Submit)
ส่งโค้ดเข้าประเมินผลบนระบบ iJudge ทันที:
```bash
python3 .op/scripts/pscp.py submit --ids <ids> --yes
```
*ระบบจะแสดงรายงานสรุปผล:*
- **Verdict**: ต้องได้ `✅ PPPPP...` (ผ่านครบทุก testcase)
- **Score**: `1000.0 / 1000.0`
- **PEP8**: `10.0 / 10.0`

---

### 7. Post-Pass One-Liner (ซิงค์สถานะ, เก็บ Archive, อัปเดต README, เช็ค Doctor)
เมื่อส่งผ่านแล้ว ให้รันคำสั่ง One-Liner นี้ทันทีเพื่อซิงค์ทั้งระบบ:
```bash
python3 .op/scripts/pscp.py status && python3 .op/scripts/pscp.py archive && python3 .op/scripts/pscp.py readme && python3 .op/scripts/pscp.py doctor
```

**หน้าที่ของแต่ละคำสั่ง:**
| คำสั่ง | หน้าที่ |
|---|---|
| `pscp.py status` | เปลี่ยนชื่อโฟลเดอร์เติม ` ✅` ท้ายชื่อ เช่น `oj/oj3599-SumOfNumber ✅/` |
| `pscp.py archive` | คัดลอกโค้ดที่ผ่านแล้วไปเก็บที่ `.op/solutions/oj<id>/main.py` |
| `pscp.py readme` | อัปเดตสถิติและสร้างตารางใน [`README.md`](file:///README.md) ใหม่ทั้งหมด |
| `pscp.py doctor` | ตรวจสอบความสอดคล้องของ repo (ต้องรายงาน `Errors: none`) |

---

### 8. Commit & Push ทั้ง 2 Branches
เนื่องจากโปรเจกต์นี้แยก `main` (โค้ดของตัวเอง) และ `OP` (worktree เครื่องมือ + data + solutions) ให้ commit และ push ทั้งสอง branch:
```bash
# 1. Commit & Push บน main
git add -A && git commit -m "feat(oj): complete Week <W> problems <ids>, update README"
git push origin main

# 2. Commit & Push บน OP
git -C .op add -A && git -C .op commit -m "feat(solutions): add <ids> solutions and course data"
git -C .op push origin OP
```

---

## 🗂️ สถาปัตยกรรมของ Repository (2 Branches)

| Branch | โฟลเดอร์ | หน้าที่ |
|---|---|---|
| `main` | root ของโปรเจกต์ | โฟลเดอร์โจทย์ (`oj/oj<id>-<Name>[ ✅]/`), Learning Logs (`oj<id>/`), `README.md` |
| `OP` | `.op/` (git worktree) | สคริปต์ (`scripts/`), ฐานข้อมูล JSON (`data/`), โค้ดเฉลยสำรอง (`solutions/`) |

---

## 📌 รูปแบบโครงสร้างโฟลเดอร์

| ประเภท | โฟลเดอร์ | ตัวอย่าง |
|---|---|---|
| โจทย์ปกติ / Midterm / Mini Exam | `oj/oj<id>-<Problem_Name>/` | `oj/oj3599-SumOfNumber/` |
| โจทย์ที่ผ่าน OJ แล้ว | มี ` ✅` ต่อท้าย | `oj/oj3599-SumOfNumber ✅/` |
| Learning Log | `oj<id>/` ที่ root (ไม่ใส่ ✅) | `oj2996/` |

---

## 📝 กรณีโจทย์ Learning Log
สำหรับโจทย์ประเภท Learning Log (มีแท็ก `[LEARNING LOG]`):
1. โฟลเดอร์จะอยู่ที่ root เช่น `oj3536/` (ไม่ใช่ใน `oj/`)
2. จะต้องมีไฟล์เอกสารเพิ่มเติม:
   - `submission.md`: บันทึกการเรียนรู้ (เขียนด้วยตนเองตาม template)
   - `ai_reflection.md`: บันทึกการใช้ AI (เขียนด้วยตนเองหากมีการใช้ AI)
3. สคริปต์ `submit` ปกติจะเว้น Learning Log ไว้ป้องกันการส่งซ้ำ หากต้องการส่งให้ระบุ `--include-learning-log`

---

## 🛠️ สรุปคำสั่งลัดที่ใช้บ่อย (Cheat Sheet)

```bash
# ทดสอบ Sample ทุกข้อในสัปดาห์
python3 .op/scripts/pscp.py test --week 14

# ทดสอบ Sample โดยใช้โค้ดจาก archive
python3 .op/scripts/pscp.py test <id> --solutions

# ตรวจสุขภาพของ repo
python3 .op/scripts/pscp.py doctor

# เปิด Web Dashboard สำหรับจัดการและดูสถิติ
python3 .op/scripts/pscp.py web
```
