# CONTRIBUTE.md — วิธีตั้งค่าโฟลเดอร์โจทย์ใหม่

คู่มือนี้อธิบายขั้นตอนการสร้างโฟลเดอร์โจทย์ใหม่ในรูปแบบที่สม่ำเสมอทั้ง repo

---

## 📌 รูปแบบชื่อโฟลเดอร์

```
oj_<problem-id>-<Problem_Name>/
```

**ตัวอย่าง:**

| โฟลเดอร์ | ความหมาย |
|---|---|
| `oj_3019-Safe_Password/` | โจทย์ OJ หมายเลข 3019 ชื่อ Safe Password |
| `oj_2999-Frame/` | โจทย์ OJ หมายเลข 2999 ชื่อ Frame |

หากโจทย์เป็น Learning Log ให้ใช้รูปแบบนี้แทน:

```
[LEARNING-LOGS]-oj_<problem-id>-<Problem_Name>/
```

**ตัวอย่าง:**

```
[LEARNING-LOGS]-oj_2996-Anagram/
```

หลังจาก OJ ผ่าน (Pass) ให้เพิ่ม ` ✅` ต่อท้ายชื่อโฟลเดอร์:

```
oj_3019-Safe_Password ✅/
```

---

## 🗂️ โครงสร้างไฟล์ในโฟลเดอร์โจทย์

### โจทย์ปกติ (ไม่ใช่ Learning Log)

```
oj_<id>-<Name>/
└── main.py          # โค้ด Python หลัก
```

### โจทย์ Learning Log

```
[LEARNING-LOGS]-oj_<id>-<Name>/
├── main.py                    # โค้ด Python หลัก
├── SUBMISSION_TEMPLATE.th.md  # Template บันทึกการแก้โจทย์ (ภาษาไทย)
├── submission.md              # บันทึกการแก้โจทย์ของตนเอง (เขียนเอง!)
└── ai_reflection.md           # reflection การใช้ AI (เฉพาะเมื่อใช้ AI)
```

> **หมายเหตุ:** `SUBMISSION_TEMPLATE.th.md` และ `submission.md` ใช้เฉพาะกับโจทย์ **Learning Log** เท่านั้น ไม่ต้องสร้างสำหรับโจทย์ปกติ

---

## 🚀 ขั้นตอนการตั้งค่าโฟลเดอร์โจทย์ใหม่

### ขั้นที่ 1 — สร้างโฟลเดอร์

**โจทย์ปกติ:**

```bash
mkdir "oj_<id>-<Problem_Name>"
```

**โจทย์ Learning Log:**

```bash
mkdir "[LEARNING-LOGS]-oj_<id>-<Problem_Name>"
```

### ขั้นที่ 2 — สร้างไฟล์ `main.py`

สร้างไฟล์ `main.py` ด้วยโครงสร้างมาตรฐานนี้:

```python
""" Problem Name """

def main():
    """Problem Name"""
    # เขียนโค้ดที่นี่

if __name__ == "__main__":
    main()
```

**กฎสำคัญ:**
- บรรทัดบนสุดต้องเป็น module-level docstring ชื่อโจทย์
- โค้ดทั้งหมดต้องอยู่ใน `def main()`
- ต้องมี docstring ชื่อโจทย์ภายใน `main()` ด้วย
- ต้องปิดท้ายด้วย `if __name__ == "__main__": main()`

### ขั้นที่ 3 — คัดลอก Template (เฉพาะ Learning Log เท่านั้น)

สำหรับโจทย์ Learning Log ให้คัดลอก `SUBMISSION_TEMPLATE.th.md` เข้าโฟลเดอร์:

```bash
cp AI-Guidelines-PSCP/templates/SUBMISSION_TEMPLATE.th.md "[LEARNING-LOGS]-oj_<id>-<Problem_Name>/SUBMISSION_TEMPLATE.th.md"
```

ตัวอย่าง:

```bash
cp AI-Guidelines-PSCP/templates/SUBMISSION_TEMPLATE.th.md "[LEARNING-LOGS]-oj_2996-Anagram/SUBMISSION_TEMPLATE.th.md"
```

จากนั้นให้กรอก `submission.md` (เขียนเอง) และ `ai_reflection.md` (ถ้าใช้ AI) ตาม template

### ขั้นที่ 4 — อัปเดต `README.md`

เพิ่มโจทย์ใหม่ในตาราง **Problem Index** ใน [README.md](README.md):

```markdown
| <id> | <Problem Name> | 🔄 In Progress |
```

เมื่อผ่าน OJ แล้ว ให้เปลี่ยนเป็น:

```markdown
| <id> | <Problem Name> | ✅ Pass |
```

และเปลี่ยนชื่อโฟลเดอร์เพิ่ม ` ✅`:

```bash
mv "oj_<id>-<Problem_Name>" "oj_<id>-<Problem_Name> ✅"
```

---

## 📋 Checklist โจทย์ใหม่

### โจทย์ปกติ

```
[ ] สร้างโฟลเดอร์ oj_<id>-<Name>/
[ ] สร้าง main.py ด้วยโครงสร้าง def main() + docstring + if __name__ guard
[ ] เพิ่มโจทย์ใน README.md ตาราง Problem Index
[ ] ทดสอบโค้ดใน VS Code ก่อนส่ง OJ
[ ] หลัง Pass: เปลี่ยนชื่อโฟลเดอร์เพิ่ม ✅ และอัปเดต README
```

### โจทย์ Learning Log

```
[ ] สร้างโฟลเดอร์ [LEARNING-LOGS]-oj_<id>-<Name>/
[ ] สร้าง main.py ด้วยโครงสร้าง def main() + docstring + if __name__ guard
[ ] คัดลอก SUBMISSION_TEMPLATE.th.md เข้าโฟลเดอร์
[ ] กรอก submission.md ด้วยตนเอง
[ ] กรอก ai_reflection.md (ถ้าใช้ AI)
[ ] เพิ่มโจทย์ใน README.md ตาราง Learning Logs
[ ] ทดสอบโค้ดใน VS Code ก่อนส่ง OJ
[ ] หลัง Pass: เปลี่ยนชื่อโฟลเดอร์เพิ่ม ✅ และอัปเดต README
```

---

## 🧪 วิธีทดสอบโค้ดใน VS Code

รันโค้ดด้วยคำสั่ง:

```bash
python "oj_<id>-<Problem_Name>/main.py"
```

หรือบน macOS อาจใช้:

```bash
python3 "oj_<id>-<Problem_Name>/main.py"
```

---

## 🗒️ สรุปรูปแบบมาตรฐาน

| ไฟล์                        | จำเป็น                             | หมายเหตุ                   |
| ----------------------------| :----------------------------------:| ---------------------------|
| `main.py`                   | ✅ ทุกโฟลเดอร์                    | โค้ดหลัก                   |
| `SUBMISSION_TEMPLATE.th.md` | เฉพาะ Learning Log                 | template สำหรับกรอก        |
| `submission.md`             | เฉพาะ Learning Log                 | เขียนเอง ห้ามให้ AI เขียน  |
| `ai_reflection.md`          | เฉพาะเมื่อใช้ AI กับ Learning Log  | เขียนเอง ห้ามให้ AI เขียน  |
