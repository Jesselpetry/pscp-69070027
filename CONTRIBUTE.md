# CONTRIBUTE.md — วิธีเพิ่มและทำโจทย์ใน repo นี้

repo นี้มี 2 branch ที่ทำหน้าที่ต่างกัน:

| Branch | อยู่ที่ | มีอะไร |
|---|---|---|
| `main` | root ของ repo | โฟลเดอร์โจทย์ (`problem.md` + `main.py`), Learning Log, `recommended/`, README |
| `OP` | worktree `.op/` (gitignored บน main) | scripts, ข้อมูลโจทย์ (JSON), คลังโค้ดที่ทำเสร็จ (`solutions/`) |

เขียนโค้ดบน `main` เท่านั้น ส่วนเครื่องมือทั้งหมดรันจาก `.op/`

---

## ⚙️ ตั้งค่าครั้งแรก

```bash
git worktree add .op OP                          # เอา branch OP มาไว้ที่ .op/
export IJUDGE_COOKIE='access_token=...'          # cookie จาก browser — เฉพาะคำสั่งที่ต่อ iJudge
python3 .op/scripts/pscp.py                      # ดูคำสั่งทั้งหมด
```

วิธีหา cookie และตัวเลือกอื่นอยู่ใน `.op/scripts/README.md`

---

## 📌 รูปแบบชื่อโฟลเดอร์

| ประเภท | โฟลเดอร์ | ตัวอย่าง |
|---|---|---|
| โจทย์ปกติ / Midterm / Mini Exam | `oj/oj<id>-<Problem_Name>/` | `oj/oj3019-Safe_Password/` |
| โจทย์ที่ผ่านแล้ว | ต่อท้าย ` ✅` | `oj/oj3019-Safe_Password ✅/` |
| Learning Log | `oj<id>/` ที่ root (ไม่ใส่ ✅) | `oj2996/` |

ชื่อ `<Problem_Name>` ของโจทย์ชื่อภาษาไทยตั้งไว้ใน `.op/data/course.json` (`folder_names`)

---

## 🗂️ ไฟล์ในโฟลเดอร์โจทย์

```
oj/oj<id>-<Name>/
├── problem.md       # สร้างจาก JSON — ห้ามแก้มือ (แก้แล้วจะโดนเขียนทับ)
└── main.py          # โค้ดของเรา — script สร้าง stub ให้ครั้งเดียว ไม่เขียนทับ

oj<id>/                          # Learning Log
├── problem.md
├── main.py
├── submission.md                # เขียนเอง! ห้ามให้ AI เขียน
└── ai_reflection.md             # เฉพาะเมื่อใช้ AI — เขียนเอง
```

`main.py` มาตรฐาน:

```python
""" Problem Name """


def main():
    """Problem Name"""
    # solution code here


if __name__ == "__main__":
    main()
```

- บรรทัดแรกเป็น module docstring ชื่อโจทย์
- โค้ดทั้งหมดอยู่ใน `def main()` ที่มี docstring
- ปิดท้ายด้วย `if __name__ == "__main__": main()`

---

## 🚀 ทำโจทย์ใหม่

### 1. ดึงโจทย์

```bash
python3 .op/scripts/pscp.py scrape --only 3586-3598   # ดึงจาก iJudge → JSON → problem.md + main.py stub
python3 .op/scripts/pscp.py render                    # (ไม่ต่อเน็ต) สร้างไฟล์ใหม่จาก JSON ที่มีอยู่
```

Learning Log: คัดลอก template มาเขียน `submission.md` เอง

```bash
cp AI-Guidelines-PSCP/templates/SUBMISSION_TEMPLATE.th.md "oj<id>/SUBMISSION_TEMPLATE.th.md"
```

### 2. เขียนและทดสอบ

```bash
python3 "oj/oj<id>-<Name>/main.py"          # รันเองใน VS Code
python3 .op/scripts/pscp.py test <id>       # รันกับ sample ทางการจาก iJudge
```

### 3. หลังผ่าน OJ

```bash
python3 .op/scripts/pscp.py scrape --fast   # อัปเดตสถานะจาก iJudge
python3 .op/scripts/pscp.py status          # เติม/ลบ ✅ ท้ายชื่อโฟลเดอร์ตามสถานะ
python3 .op/scripts/pscp.py archive         # เก็บโค้ดที่เสร็จแล้วเข้า .op/solutions/
python3 .op/scripts/pscp.py readme          # สร้าง README ใหม่ (ห้ามแก้ README มือ)
python3 .op/scripts/pscp.py doctor          # ตรวจว่าไม่มีอะไรหลุด
```

แล้ว commit แยกกันทั้ง 2 branch:

```bash
git add -A && git commit -m "feat(oj): ..."              # main
git -C .op add -A && git -C .op commit -m "chore: ..."   # OP
```

---

## 📋 Checklist

### โจทย์ปกติ

```text
[ ] มีโฟลเดอร์ oj/oj<id>-<Name>/ พร้อม problem.md + main.py (scrape/render สร้างให้)
[ ] เขียน main.py ตามโครงสร้าง def main() + docstring + if __name__ guard
[ ] ทดสอบใน VS Code และ pscp.py test <id>
[ ] หลัง Pass: scrape --fast → status → archive → readme
```

### โจทย์ Learning Log

```text
[ ] มีโฟลเดอร์ oj<id>/ พร้อม problem.md + main.py
[ ] คัดลอก SUBMISSION_TEMPLATE.th.md แล้วเขียน submission.md เอง
[ ] เขียน ai_reflection.md เอง (ถ้าใช้ AI)
[ ] ทดสอบใน VS Code และ pscp.py test <id>
[ ] หลัง Pass: scrape --fast → archive → readme
```

---

## 🗒️ สรุป

| ไฟล์ | ใครเขียน | หมายเหตุ |
|---|---|---|
| `problem.md` | script | generate จาก `.op/data/all_problems_detail.json` |
| `main.py` | เรา | script สร้าง stub ครั้งเดียว |
| `submission.md` | เรา | เฉพาะ Learning Log — ห้ามให้ AI เขียน |
| `ai_reflection.md` | เรา | เฉพาะ Learning Log ที่ใช้ AI — ห้ามให้ AI เขียน |
| `README.md` | script | `pscp.py readme` |
| `recommended/` | เรา | script ไม่แตะ |
