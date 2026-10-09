<div align="center">
  <img src="public/IT-KMITL-Logo.png" alt="IT KMITL Logo" width="420"/>
</div>

---

# PSCP — Problem Solving and Computer Programming

**การแก้ปัญหาและการโปรแกรมคอมพิวเตอร์ (06066303)**
3 Credits (2-2-5) · Bachelor's Degree · School of Information Technology, KMITL

---

## 👤 Student Information

| Field | Details |
| :--- | :---|
| **Name (TH)** | นายฉัททัณฑ์ เพททริ |
| **Name (EN)** | Chatan Petry |
| **Student ID** | 69070027 |
| **Email** | 69070027@kmitl.ac.th |
| **Faculty** | คณะเทคโนโลยีสารสนเทศ (School of Information Technology) |
| **Institution** | สถาบันเทคโนโลยีพระจอมเกล้าเจ้าคุณทหารลาดกระบัง (KMITL) |

---

## 📊 Overall Progress Dashboard

- **Total Problems Tracked**: `224`
- **✅ Solved / Passed**: `106` (47.3%)
- **🔄 In Progress / Pending**: `118`

### 📅 Weekly Progress (นับตั้งแต่สัปดาห์แรกที่เปิดเทอม)

| Week | Topic / Focus | Total | Passed | In Progress | Completion |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **Week 1** | บทนำ ตัวแปร และการรับส่งข้อมูลพื้นฐาน (Basic I/O & Variables) | 15 | 15 | 0 | **100.0%** |
| **Week 2** | การทำงานแบบมีเงื่อนไขพื้นฐาน (Basic Conditionals & Logic) | 26 | 26 | 0 | **100.0%** |
| **Week 3** | การทำงานแบบมีเงื่อนไขขั้นสูง (Nested Conditionals & Advanced Logic) | 15 | 15 | 0 | **100.0%** |
| **Week 4** | การทำงานซ้ำแบบ While Loop และตัวแปรสะสม (While Loops & Accumulators) | 15 | 6 | 9 | **40.0%** |
| **Week 5** | การทำงานซ้ำแบบ For Loop และลูปซ้อนลูป (For Loops & Geometry Drawing) | 15 | 15 | 0 | **100.0%** |
| **Week 6** | ลูปขั้นสูง สตริง และลำดับอนุกรม (Advanced Loops, Strings & Sequences) | 13 | 13 | 0 | **100.0%** |
| **Week 7** | ชุดข้อสอบจำลองกลางภาค (Midterm Mock Exam) | 9 | 0 | 9 | **0.0%** |
| **Week 8** | ลิสต์และการประมวลผลสตริงขั้นสูง (Lists & Advanced Sequence Operations) | 12 | 12 | 0 | **100.0%** |
| **Week 9** | ลิสต์ขั้นสูงและการประยุกต์ใช้งาน (Advanced Lists & Applied Algorithms) | 15 | 0 | 15 | **0.0%** |
| **Week 10** | ทูเพิล ลิสต์ 2 มิติ และการเรียงลำดับ (Tuples, 2D Lists & Sorting) | 16 | 0 | 16 | **0.0%** |
| **Week 11** | การจำลองการทำงานและเซต (Simulation, String Processing & Sets) | 16 | 0 | 16 | **0.0%** |
| **Week 12** | ดิกชันนารีและเซตขั้นสูง (Advanced Dictionaries, Sets & Algorithms) | 16 | 0 | 16 | **0.0%** |
| **Week 13** | การเรียกซ้ำ (Recursion & Divide and Conquer) | 13 | 2 | 11 | **15.4%** |
| **Week 14** | ชุดข้อสอบย่อยจำลอง (Mini Exam / Mock Test) | 28 | 2 | 26 | **7.1%** |

### 🏷️ Category Breakdown

| Category | Total | Passed | In Progress |
| :--- | :---: | :---: | :---: |
| **🎯 Midterm Mock Exam** | 9 | 0 | 9 |
| **📝 Mini Exam** | 26 | 0 | 26 |
| **🌟 Recommended Problems** | 10 | 10 | 0 |
| **📓 Learning Logs** | 36 | 21 | 15 |

---

## 📁 Repository Structure

```
pscp-69070027/           # branch main — โจทย์ + โค้ดของตัวเอง
├── oj/                  # โจทย์ปกติ + Midterm + Mini Exam (188 โฟลเดอร์): oj<id>-<Name>/ → problem.md, main.py (ลงท้าย ✅ = ผ่านแล้ว)
├── oj<id>/              # Learning Log (36 โฟลเดอร์): main.py, problem.md, submission.md (+ ai_reflection.md)
├── recommended/         # สรุปโจทย์แนะนำที่เขียนเอง (10 ข้อ) + สรุป ce-kmitl
├── AI-Guidelines-PSCP/  # แนวทางการใช้ AI ของรายวิชา
├── public/              # รูปประกอบ README
├── README.md            # generated โดย update_readme.py — ห้ามแก้มือ
├── CONTRIBUTE.md        # วิธีเพิ่มโจทย์และส่งงาน
└── .op/                 # worktree ของ branch OP (gitignored บน main)
    ├── scripts/         # 10 scripts + ijudge/ (shared package)
    ├── data/            # course.json, oj_problems.json (224 ข้อ), all_problems_detail.json (223 ข้อ), html_cache/ (gitignored)
    ├── solutions/       # เฉลยครบ 224 ข้อ: oj<id>/main.py
    └── docs/            # PLAN.md
```

---

## 🌿 Branches

| Branch | บทบาท | Commit ล่าสุด | นำ / ตาม อีก branch | ยังไม่ push |
| :--- | :--- | :--- | :---: | :---: |
| `main` | โจทย์ + โค้ดของตัวเอง | `9a183c1` · 2026-10-09 | 5 / 13 | 1 |
| `OP` | scripts + data + เฉลยครบใน `solutions/` | `c4f611f` · 2026-10-09 | 13 / 5 | 1 |

```bash
git worktree add .op OP              # ครั้งเดียว ถ้ายังไม่มี
python3 .op/scripts/pscp.py readme   # รัน script จาก root ของ repo
```

---

## 🎯 1. Midterm Mock Exam Problems (Week 7)

ชุดข้อสอบจำลอง Midterm PSCP พร้อมคำอธิบายโจทย์ ข้อกำหนด และตัวอย่างเทสเคส

| OJ ID | Problem Name | Status | Problem Folder | Problem Spec | Solution Code |
| :---: | :--- | :---: | :--- | :---: | :---: |
| **3274** | Triangle | 🔄 *In Progress* | [`oj3274-MIDTERM_Triangle`](oj/oj3274-MIDTERM_Triangle) | [`problem.md`](oj/oj3274-MIDTERM_Triangle/problem.md) | [`main.py`](oj/oj3274-MIDTERM_Triangle/main.py) |
| **3275** | PIZZA TIME | 🔄 *In Progress* | [`oj3275-MIDTERM_Pizza_Time`](oj/oj3275-MIDTERM_Pizza_Time) | [`problem.md`](oj/oj3275-MIDTERM_Pizza_Time/problem.md) | [`main.py`](oj/oj3275-MIDTERM_Pizza_Time/main.py) |
| **3276** | FakeThaiPlus | 🔄 *In Progress* | [`oj3276-MIDTERM_FakeThaiPlus`](oj/oj3276-MIDTERM_FakeThaiPlus) | [`problem.md`](oj/oj3276-MIDTERM_FakeThaiPlus/problem.md) | [`main.py`](oj/oj3276-MIDTERM_FakeThaiPlus/main.py) |
| **3277** | RealThaiPlus | 🔄 *In Progress* | [`oj3277-MIDTERM_RealThaiPlus`](oj/oj3277-MIDTERM_RealThaiPlus) | [`problem.md`](oj/oj3277-MIDTERM_RealThaiPlus/problem.md) | [`main.py`](oj/oj3277-MIDTERM_RealThaiPlus/main.py) |
| **3278** | Units | 🔄 *In Progress* | [`oj3278-MIDTERM_Units`](oj/oj3278-MIDTERM_Units) | [`problem.md`](oj/oj3278-MIDTERM_Units/problem.md) | [`main.py`](oj/oj3278-MIDTERM_Units/main.py) |
| **3279** | PM WATCH | 🔄 *In Progress* | [`oj3279-MIDTERM_PM_Watch`](oj/oj3279-MIDTERM_PM_Watch) | [`problem.md`](oj/oj3279-MIDTERM_PM_Watch/problem.md) | [`main.py`](oj/oj3279-MIDTERM_PM_Watch/main.py) |
| **3280** | CODE CLEANER | 🔄 *In Progress* | [`oj3280-MIDTERM_Code_Cleaner`](oj/oj3280-MIDTERM_Code_Cleaner) | [`problem.md`](oj/oj3280-MIDTERM_Code_Cleaner/problem.md) | [`main.py`](oj/oj3280-MIDTERM_Code_Cleaner/main.py) |
| **3281** | ijudge-itkmitl | 🔄 *In Progress* | [`oj3281-MIDTERM_ijudge-itkmitl`](oj/oj3281-MIDTERM_ijudge-itkmitl) | [`problem.md`](oj/oj3281-MIDTERM_ijudge-itkmitl/problem.md) | [`main.py`](oj/oj3281-MIDTERM_ijudge-itkmitl/main.py) |
| **3282** | Stats | 🔄 *In Progress* | [`oj3282-MIDTERM_Stats`](oj/oj3282-MIDTERM_Stats) | [`problem.md`](oj/oj3282-MIDTERM_Stats/problem.md) | [`main.py`](oj/oj3282-MIDTERM_Stats/main.py) |

---

## 🌟 2. Recommended Problems (คลังโจทย์แนะนำ 10 ข้อ)

โจทย์สำคัญ 10 ข้อที่รวบรวมเทคนิคสำคัญของภาษา Python พร้อมคำอธิบายและแนวคิดอย่างละเอียด

| OJ ID | Problem Name | Week | Status | Recommended Folder | Standard Folder | Problem Spec | Solution Code |
| :---: | :--- | :---: | :---: | :--- | :--- | :---: | :---: |
| **2996** | สลับตัวอักษร | Week 2 | ✅ **Passed** | [`oj2996-Swap_Characters`](recommended/oj2996-Swap_Characters) | [`oj2996`](oj2996) | [`problem.md`](recommended/oj2996-Swap_Characters/problem.md) | [`main.py`](recommended/oj2996-Swap_Characters/main.py) |
| **2997** | Elo | Week 2 | ✅ **Passed** | [`oj2997-Elo`](recommended/oj2997-Elo) | [`oj2997-Elo ✅`](oj/oj2997-Elo%20%E2%9C%85) | [`problem.md`](recommended/oj2997-Elo/problem.md) | [`main.py`](recommended/oj2997-Elo/main.py) |
| **2998** | EuclideanDistance2D | Week 2 | ✅ **Passed** | [`oj2998-EuclideanDistance2D`](recommended/oj2998-EuclideanDistance2D) | [`oj2998-EuclideanDistance2D ✅`](oj/oj2998-EuclideanDistance2D%20%E2%9C%85) | [`problem.md`](recommended/oj2998-EuclideanDistance2D/problem.md) | [`main.py`](recommended/oj2998-EuclideanDistance2D/main.py) |
| **3019** | Safe Password | Week 2 | ✅ **Passed** | [`oj3019-Safe_Password`](recommended/oj3019-Safe_Password) | [`oj3019-Safe_Password ✅`](oj/oj3019-Safe_Password%20%E2%9C%85) | [`problem.md`](recommended/oj3019-Safe_Password/problem.md) | [`main.py`](recommended/oj3019-Safe_Password/main.py) |
| **3020** | Coke | Week 2 | ✅ **Passed** | [`oj3020-Coke`](recommended/oj3020-Coke) | [`oj3020-Coke ✅`](oj/oj3020-Coke%20%E2%9C%85) | [`problem.md`](recommended/oj3020-Coke/problem.md) | [`main.py`](recommended/oj3020-Coke/main.py) |
| **3022** | Temperature | Week 2 | ✅ **Passed** | [`oj3022-Temperature`](recommended/oj3022-Temperature) | [`oj3022`](oj3022) | [`problem.md`](recommended/oj3022-Temperature/problem.md) | [`main.py`](recommended/oj3022-Temperature/main.py) |
| **3159** | Factorial | Week 5 | ✅ **Passed** | [`oj3159-Factorial`](recommended/oj3159-Factorial) | [`oj3159-Factorial ✅`](oj/oj3159-Factorial%20%E2%9C%85) | [`problem.md`](recommended/oj3159-Factorial/problem.md) | [`main.py`](recommended/oj3159-Factorial/main.py) |
| **3167** | FizzBuzz | Week 5 | ✅ **Passed** | [`oj3167-FizzBuzz`](recommended/oj3167-FizzBuzz) | [`oj3167-FizzBuzz ✅`](oj/oj3167-FizzBuzz%20%E2%9C%85) | [`problem.md`](recommended/oj3167-FizzBuzz/problem.md) | [`main.py`](recommended/oj3167-FizzBuzz/main.py) |
| **3226** | Inflation | Week 6 | ✅ **Passed** | [`oj3226-Inflation`](recommended/oj3226-Inflation) | [`oj3226-Inflation ✅`](oj/oj3226-Inflation%20%E2%9C%85) | [`problem.md`](recommended/oj3226-Inflation/problem.md) | [`main.py`](recommended/oj3226-Inflation/main.py) |
| **3237** | สามเหลี่ยม | Week 6 | ✅ **Passed** | [`oj3237-Triangle`](recommended/oj3237-Triangle) | [`oj3237-Triangle ✅`](oj/oj3237-Triangle%20%E2%9C%85) | [`problem.md`](recommended/oj3237-Triangle/problem.md) | [`main.py`](recommended/oj3237-Triangle/main.py) |

---

## 📓 3. Learning Logs (บันทึกการเรียนรู้)

โจทย์ที่ต้องส่ง Learning Log พร้อมบันทึก `submission.md` และการสะท้อนความคิด

| OJ ID | Problem Name | Week | Status | Learning Log Folder | Problem Spec | Submission Doc | Code |
| :---: | :--- | :---: | :---: | :--- | :---: | :---: | :---: |
| **2996** | สลับตัวอักษร | Week 2 | ✅ **Passed** | [`oj2996`](oj2996) | [`problem.md`](oj2996/problem.md) | [`submission.md`](oj2996/submission.md) | [`main.py`](oj2996/main.py) |
| **3011** | Colors | Week 1 | ✅ **Passed** | [`oj3011`](oj3011) | [`problem.md`](oj3011/problem.md) | [`submission.md`](oj3011/submission.md) | [`main.py`](oj3011/main.py) |
| **3017** | Bill | Week 1 | ✅ **Passed** | [`oj3017`](oj3017) | [`problem.md`](oj3017/problem.md) | [`submission.md`](oj3017/submission.md) | [`main.py`](oj3017/main.py) |
| **3022** | Temperature | Week 2 | ✅ **Passed** | [`oj3022`](oj3022) | [`problem.md`](oj3022/problem.md) | [`submission.md`](oj3022/submission.md) | [`main.py`](oj3022/main.py) |
| **3024** | SurprisingVote | Week 2 | ✅ **Passed** | [`oj3024`](oj3024) | [`problem.md`](oj3024/problem.md) | [`submission.md`](oj3024/submission.md) | [`main.py`](oj3024/main.py) |
| **3025** | Season | Week 2 | ✅ **Passed** | [`oj3025`](oj3025) | [`problem.md`](oj3025/problem.md) | [`submission.md`](oj3025/submission.md) | [`main.py`](oj3025/main.py) |
| **3031** | Ink | Week 2 | ✅ **Passed** | [`oj3031`](oj3031) | [`problem.md`](oj3031/problem.md) | - | [`main.py`](oj3031/main.py) |
| **3036** | ปราสาท | Week 2 | ✅ **Passed** | [`oj3036`](oj3036) | [`problem.md`](oj3036/problem.md) | - | [`main.py`](oj3036/main.py) |
| **3042** | หาร 10 | Week 2 | ✅ **Passed** | [`oj3042`](oj3042) | [`problem.md`](oj3042/problem.md) | [`submission.md`](oj3042/submission.md) | [`main.py`](oj3042/main.py) |
| **3058** | BrickBridge | Week 3 | ✅ **Passed** | [`oj3058`](oj3058) | [`problem.md`](oj3058/problem.md) | [`submission.md`](oj3058/submission.md) | [`main.py`](oj3058/main.py) |
| **3071** | จำนวนในช่วง ที่หารด้วย d เหลือเศษ r | Week 3 | ✅ **Passed** | [`oj3071`](oj3071) | [`problem.md`](oj3071/problem.md) | [`submission.md`](oj3071/submission.md) | [`main.py`](oj3071/main.py) |
| **3072** | A-E-I-O-U | Week 3 | ✅ **Passed** | [`oj3072`](oj3072) | [`problem.md`](oj3072/problem.md) | [`submission.md`](oj3072/submission.md) | [`main.py`](oj3072/main.py) |
| **3110** | สงคราม...ส่งด่วน | Week 4 | 🔄 *In Progress* | [`oj3110`](oj3110) | [`problem.md`](oj3110/problem.md) | - | [`main.py`](oj3110/main.py) |
| **3111** | สหกรณ์โรงเรียน | Week 4 | 🔄 *In Progress* | [`oj3111`](oj3111) | [`problem.md`](oj3111/problem.md) | - | [`main.py`](oj3111/main.py) |
| **3115** | Arcade of Time: Store Check | Week 4 | 🔄 *In Progress* | [`oj3115`](oj3115) | [`problem.md`](oj3115/problem.md) | - | [`main.py`](oj3115/main.py) |
| **3135** | ของขวัญและขโมย | Week 5 | ✅ **Passed** | [`oj3135`](oj3135) | [`problem.md`](oj3135/problem.md) | [`submission.md`](oj3135/submission.md) | [`main.py`](oj3135/main.py) |
| **3157** | เกมสะสมแต้ม | Week 5 | ✅ **Passed** | [`oj3157`](oj3157) | [`problem.md`](oj3157/problem.md) | [`submission.md`](oj3157/submission.md) | [`main.py`](oj3157/main.py) |
| **3160** | หาจำนวนเฉพาะ | Week 5 | ✅ **Passed** | [`oj3160`](oj3160) | [`problem.md`](oj3160/problem.md) | [`submission.md`](oj3160/submission.md) | [`main.py`](oj3160/main.py) |
| **3227** | ไพ่ 44 ใบ | Week 6 | ✅ **Passed** | [`oj3227`](oj3227) | [`problem.md`](oj3227/problem.md) | [`submission.md`](oj3227/submission.md) | [`main.py`](oj3227/main.py) |
| **3232** | กบน้อยกระโดด | Week 6 | ✅ **Passed** | [`oj3232`](oj3232) | [`problem.md`](oj3232/problem.md) | [`submission.md`](oj3232/submission.md) | [`main.py`](oj3232/main.py) |
| **3233** | สลากกินแบ่ง | Week 6 | ✅ **Passed** | [`oj3233`](oj3233) | [`problem.md`](oj3233/problem.md) | [`submission.md`](oj3233/submission.md) | [`main.py`](oj3233/main.py) |
| **3293** | BigFrame | Week 8 | ✅ **Passed** | [`oj3293`](oj3293) | [`problem.md`](oj3293/problem.md) | - | [`main.py`](oj3293/main.py) |
| **3296** | RGB Mixed | Week 8 | ✅ **Passed** | [`oj3296`](oj3296) | [`problem.md`](oj3296/problem.md) | - | [`main.py`](oj3296/main.py) |
| **3299** | แปลงดอกไม้ | Week 8 | ✅ **Passed** | [`oj3299`](oj3299) | [`problem.md`](oj3299/problem.md) | - | [`main.py`](oj3299/main.py) |
| **3355** | Shorten | Week 9 | 🔄 *In Progress* | [`oj3355`](oj3355) | [`problem.md`](oj3355/problem.md) | - | [`main.py`](oj3355/main.py) |
| **3357** | Giraffe | Week 9 | 🔄 *In Progress* | [`oj3357`](oj3357) | [`problem.md`](oj3357/problem.md) | - | [`main.py`](oj3357/main.py) |
| **3360** | หั่นขนมปัง | Week 9 | 🔄 *In Progress* | [`oj3360`](oj3360) | [`problem.md`](oj3360/problem.md) | - | [`main.py`](oj3360/main.py) |
| **3381** | Point Sorting | Week 10 | 🔄 *In Progress* | [`oj3381`](oj3381) | [`problem.md`](oj3381/problem.md) | - | [`main.py`](oj3381/main.py) |
| **3386** | Duplicate I | Week 10 | 🔄 *In Progress* | [`oj3386`](oj3386) | [`problem.md`](oj3386/problem.md) | - | [`main.py`](oj3386/main.py) |
| **3394** | ส่งต่อ | Week 10 | 🔄 *In Progress* | [`oj3394`](oj3394) | [`problem.md`](oj3394/problem.md) | - | [`main.py`](oj3394/main.py) |
| **3476** | CuteCat CuteFox | Week 11 | 🔄 *In Progress* | [`oj3476`](oj3476) | [`problem.md`](oj3476/problem.md) | - | [`main.py`](oj3476/main.py) |
| **3477** | Pad Thai | Week 11 | 🔄 *In Progress* | [`oj3477`](oj3477) | [`problem.md`](oj3477/problem.md) | - | [`main.py`](oj3477/main.py) |
| **3484** | หุ่นยนต์เคาะเสียงกระเบื้อง | Week 11 | 🔄 *In Progress* | [`oj3484`](oj3484) | [`problem.md`](oj3484/problem.md) | - | [`main.py`](oj3484/main.py) |
| **3536** | isPrime_large | Week 12 | 🔄 *In Progress* | [`oj3536`](oj3536) | [`problem.md`](oj3536/problem.md) | - | [`main.py`](oj3536/main.py) |
| **3537** | Impostor | Week 12 | 🔄 *In Progress* | [`oj3537`](oj3537) | [`problem.md`](oj3537/problem.md) | - | [`main.py`](oj3537/main.py) |
| **3538** | B - Fully pair? | Week 12 | 🔄 *In Progress* | [`oj3538`](oj3538) | [`problem.md`](oj3538/problem.md) | - | [`main.py`](oj3538/main.py) |

---

## 💻 4. Standard OJ Problems (จำแนกตามสัปดาห์ตั้งแต่เปิดเทอม)

### 📅 Week 1: บทนำ ตัวแปร และการรับส่งข้อมูลพื้นฐาน (Basic I/O & Variables)

> รวม `13` ข้อ (ผ่านแล้ว `13/13`)

| OJ ID | Problem Name | Status | Folder Link | Problem Spec | Solution Code |
| :---: | :--- | :---: | :--- | :---: | :---: |
| **2981** | สวัสดี: ชื่อ | ✅ **Passed** | [`oj2981-Sawasdee_Name ✅`](oj/oj2981-Sawasdee_Name%20%E2%9C%85) | - | [`main.py`](oj/oj2981-Sawasdee_Name%20%E2%9C%85/main.py) |
| **2988** | การตรวจสอบบัตรประชาชน | ✅ **Passed** | [`oj2988-National_ID_Verification ✅`](oj/oj2988-National_ID_Verification%20%E2%9C%85) | [`problem.md`](oj/oj2988-National_ID_Verification%20%E2%9C%85/problem.md) | [`main.py`](oj/oj2988-National_ID_Verification%20%E2%9C%85/main.py) |
| **2992** | สลับหมายเลข | ✅ **Passed** | [`oj2992-Swap_Number ✅`](oj/oj2992-Swap_Number%20%E2%9C%85) | [`problem.md`](oj/oj2992-Swap_Number%20%E2%9C%85/problem.md) | [`main.py`](oj/oj2992-Swap_Number%20%E2%9C%85/main.py) |
| **2995** | การตรวจสอบบัตรนักศึกษา | ✅ **Passed** | [`oj2995-Student_Card_Verification ✅`](oj/oj2995-Student_Card_Verification%20%E2%9C%85) | [`problem.md`](oj/oj2995-Student_Card_Verification%20%E2%9C%85/problem.md) | [`main.py`](oj/oj2995-Student_Card_Verification%20%E2%9C%85/main.py) |
| **2999** | Frame | ✅ **Passed** | [`oj2999-Frame ✅`](oj/oj2999-Frame%20%E2%9C%85) | [`problem.md`](oj/oj2999-Frame%20%E2%9C%85/problem.md) | [`main.py`](oj/oj2999-Frame%20%E2%9C%85/main.py) |
| **3002** | Cyan's password generator | ✅ **Passed** | [`oj3002-Cyans_password_generator ✅`](oj/oj3002-Cyans_password_generator%20%E2%9C%85) | [`problem.md`](oj/oj3002-Cyans_password_generator%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3002-Cyans_password_generator%20%E2%9C%85/main.py) |
| **3004** | หาระยะทางระหว่างจุด 3D | ✅ **Passed** | [`oj3004-Distance_3D ✅`](oj/oj3004-Distance_3D%20%E2%9C%85) | [`problem.md`](oj/oj3004-Distance_3D%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3004-Distance_3D%20%E2%9C%85/main.py) |
| **3005** | กระต่ายน้อยจ่ายตลาด | ✅ **Passed** | [`oj3005-Rabbit_Shopping ✅`](oj/oj3005-Rabbit_Shopping%20%E2%9C%85) | [`problem.md`](oj/oj3005-Rabbit_Shopping%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3005-Rabbit_Shopping%20%E2%9C%85/main.py) |
| **3006** | Gift I | ✅ **Passed** | [`oj3006-Gift_I ✅`](oj/oj3006-Gift_I%20%E2%9C%85) | [`problem.md`](oj/oj3006-Gift_I%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3006-Gift_I%20%E2%9C%85/main.py) |
| **3008** | Heron of Alexandria | ✅ **Passed** | [`oj3008-Heron_of_Alexandria ✅`](oj/oj3008-Heron_of_Alexandria%20%E2%9C%85) | [`problem.md`](oj/oj3008-Heron_of_Alexandria%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3008-Heron_of_Alexandria%20%E2%9C%85/main.py) |
| **3010** | Quadrant | ✅ **Passed** | [`oj3010-Quadrant ✅`](oj/oj3010-Quadrant%20%E2%9C%85) | [`problem.md`](oj/oj3010-Quadrant%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3010-Quadrant%20%E2%9C%85/main.py) |
| **3015** | Pro | ✅ **Passed** | [`oj3015-Pro ✅`](oj/oj3015-Pro%20%E2%9C%85) | [`problem.md`](oj/oj3015-Pro%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3015-Pro%20%E2%9C%85/main.py) |
| **3016** | Seven | ✅ **Passed** | [`oj3016-Seven ✅`](oj/oj3016-Seven%20%E2%9C%85) | [`problem.md`](oj/oj3016-Seven%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3016-Seven%20%E2%9C%85/main.py) |

### 📅 Week 2: การทำงานแบบมีเงื่อนไขพื้นฐาน (Basic Conditionals & Logic)

> รวม `19` ข้อ (ผ่านแล้ว `19/19`)

| OJ ID | Problem Name | Status | Folder Link | Problem Spec | Solution Code |
| :---: | :--- | :---: | :--- | :---: | :---: |
| **2997** | Elo | ✅ **Passed** | [`oj2997-Elo ✅`](oj/oj2997-Elo%20%E2%9C%85) | [`problem.md`](oj/oj2997-Elo%20%E2%9C%85/problem.md) | [`main.py`](oj/oj2997-Elo%20%E2%9C%85/main.py) |
| **2998** | EuclideanDistance2D | ✅ **Passed** | [`oj2998-EuclideanDistance2D ✅`](oj/oj2998-EuclideanDistance2D%20%E2%9C%85) | [`problem.md`](oj/oj2998-EuclideanDistance2D%20%E2%9C%85/problem.md) | [`main.py`](oj/oj2998-EuclideanDistance2D%20%E2%9C%85/main.py) |
| **3014** | Milk | ✅ **Passed** | [`oj3014-Milk ✅`](oj/oj3014-Milk%20%E2%9C%85) | [`problem.md`](oj/oj3014-Milk%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3014-Milk%20%E2%9C%85/main.py) |
| **3018** | RectangleArea | ✅ **Passed** | [`oj3018-RectangleArea ✅`](oj/oj3018-RectangleArea%20%E2%9C%85) | [`problem.md`](oj/oj3018-RectangleArea%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3018-RectangleArea%20%E2%9C%85/main.py) |
| **3019** | Safe Password | ✅ **Passed** | [`oj3019-Safe_Password ✅`](oj/oj3019-Safe_Password%20%E2%9C%85) | [`problem.md`](oj/oj3019-Safe_Password%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3019-Safe_Password%20%E2%9C%85/main.py) |
| **3020** | Coke | ✅ **Passed** | [`oj3020-Coke ✅`](oj/oj3020-Coke%20%E2%9C%85) | [`problem.md`](oj/oj3020-Coke%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3020-Coke%20%E2%9C%85/main.py) |
| **3021** | OverlapCircle | ✅ **Passed** | [`oj3021-OverlapCircle ✅`](oj/oj3021-OverlapCircle%20%E2%9C%85) | [`problem.md`](oj/oj3021-OverlapCircle%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3021-OverlapCircle%20%E2%9C%85/main.py) |
| **3023** | Calculator | ✅ **Passed** | [`oj3023-Calculator ✅`](oj/oj3023-Calculator%20%E2%9C%85) | [`problem.md`](oj/oj3023-Calculator%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3023-Calculator%20%E2%9C%85/main.py) |
| **3027** | กระต่ายน้อยล้อมรั้วลวดหนาม | ✅ **Passed** | [`oj3027-Carrot_Farm_Fence ✅`](oj/oj3027-Carrot_Farm_Fence%20%E2%9C%85) | [`problem.md`](oj/oj3027-Carrot_Farm_Fence%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3027-Carrot_Farm_Fence%20%E2%9C%85/main.py) |
| **3030** | ฉันจะเป็น Saitama ให้ได้เลย | ✅ **Passed** | [`oj3030-Saitama ✅`](oj/oj3030-Saitama%20%E2%9C%85) | [`problem.md`](oj/oj3030-Saitama%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3030-Saitama%20%E2%9C%85/main.py) |
| **3032** | คะแนนสอบ | ✅ **Passed** | [`oj3032-Exam_Score ✅`](oj/oj3032-Exam_Score%20%E2%9C%85) | [`problem.md`](oj/oj3032-Exam_Score%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3032-Exam_Score%20%E2%9C%85/main.py) |
| **3033** | กระดาษห่อของขวัญ | ✅ **Passed** | [`oj3033-Gift_Wrapping_Paper ✅`](oj/oj3033-Gift_Wrapping_Paper%20%E2%9C%85) | [`problem.md`](oj/oj3033-Gift_Wrapping_Paper%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3033-Gift_Wrapping_Paper%20%E2%9C%85/main.py) |
| **3034** | พอด | ✅ **Passed** | [`oj3034-Pod ✅`](oj/oj3034-Pod%20%E2%9C%85) | [`problem.md`](oj/oj3034-Pod%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3034-Pod%20%E2%9C%85/main.py) |
| **3035** | ฟิลเตอร์ AR TikTok | ✅ **Passed** | [`oj3035-TikTok_AR_Filter ✅`](oj/oj3035-TikTok_AR_Filter%20%E2%9C%85) | [`problem.md`](oj/oj3035-TikTok_AR_Filter%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3035-TikTok_AR_Filter%20%E2%9C%85/main.py) |
| **3037** | ค่าสูงสุด | ✅ **Passed** | [`oj3037-Max_Value ✅`](oj/oj3037-Max_Value%20%E2%9C%85) | [`problem.md`](oj/oj3037-Max_Value%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3037-Max_Value%20%E2%9C%85/main.py) |
| **3038** | ค่าน้อยที่สุด | ✅ **Passed** | [`oj3038-Min_Value ✅`](oj/oj3038-Min_Value%20%E2%9C%85) | [`problem.md`](oj/oj3038-Min_Value%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3038-Min_Value%20%E2%9C%85/main.py) |
| **3039** | ค่าน้อยที่สุด (4 ค่า) | ✅ **Passed** | [`oj3039-Min_Value_4 ✅`](oj/oj3039-Min_Value_4%20%E2%9C%85) | [`problem.md`](oj/oj3039-Min_Value_4%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3039-Min_Value_4%20%E2%9C%85/main.py) |
| **3040** | แลกเปลี่ยนเงิน | ✅ **Passed** | [`oj3040-Coin ✅`](oj/oj3040-Coin%20%E2%9C%85) | [`problem.md`](oj/oj3040-Coin%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3040-Coin%20%E2%9C%85/main.py) |
| **3041** | หารลงตัว | ✅ **Passed** | [`oj3041-Divisible ✅`](oj/oj3041-Divisible%20%E2%9C%85) | [`problem.md`](oj/oj3041-Divisible%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3041-Divisible%20%E2%9C%85/main.py) |

### 📅 Week 3: การทำงานแบบมีเงื่อนไขขั้นสูง (Nested Conditionals & Advanced Logic)

> รวม `12` ข้อ (ผ่านแล้ว `12/12`)

| OJ ID | Problem Name | Status | Folder Link | Problem Spec | Solution Code |
| :---: | :--- | :---: | :--- | :---: | :---: |
| **3059** | ผลการสอบ | ✅ **Passed** | [`oj3059-Exam_Result ✅`](oj/oj3059-Exam_Result%20%E2%9C%85) | [`problem.md`](oj/oj3059-Exam_Result%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3059-Exam_Result%20%E2%9C%85/main.py) |
| **3060** | การตรวจสอบสระ | ✅ **Passed** | [`oj3060-Vowel_Verification ✅`](oj/oj3060-Vowel_Verification%20%E2%9C%85) | [`problem.md`](oj/oj3060-Vowel_Verification%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3060-Vowel_Verification%20%E2%9C%85/main.py) |
| **3061** | ผ่าน/ไม่ผ่าน | ✅ **Passed** | [`oj3061-Pass_Fail ✅`](oj/oj3061-Pass_Fail%20%E2%9C%85) | [`problem.md`](oj/oj3061-Pass_Fail%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3061-Pass_Fail%20%E2%9C%85/main.py) |
| **3062** | ค่าตั๋ว | ✅ **Passed** | [`oj3062-Ticket_Price ✅`](oj/oj3062-Ticket_Price%20%E2%9C%85) | [`problem.md`](oj/oj3062-Ticket_Price%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3062-Ticket_Price%20%E2%9C%85/main.py) |
| **3063** | รหัสเซฟ | ✅ **Passed** | [`oj3063-Safe_Code ✅`](oj/oj3063-Safe_Code%20%E2%9C%85) | [`problem.md`](oj/oj3063-Safe_Code%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3063-Safe_Code%20%E2%9C%85/main.py) |
| **3064** | วันเกิด | ✅ **Passed** | [`oj3064-Birthday ✅`](oj/oj3064-Birthday%20%E2%9C%85) | [`problem.md`](oj/oj3064-Birthday%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3064-Birthday%20%E2%9C%85/main.py) |
| **3065** | ตัวเลขโรมันแบบง่าย | ✅ **Passed** | [`oj3065-Simple_Roman_Numerals ✅`](oj/oj3065-Simple_Roman_Numerals%20%E2%9C%85) | [`problem.md`](oj/oj3065-Simple_Roman_Numerals%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3065-Simple_Roman_Numerals%20%E2%9C%85/main.py) |
| **3066** | เหมือนกันหมด | ✅ **Passed** | [`oj3066-All_Same ✅`](oj/oj3066-All_Same%20%E2%9C%85) | [`problem.md`](oj/oj3066-All_Same%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3066-All_Same%20%E2%9C%85/main.py) |
| **3067** | การเพิ่ม/ลด | ✅ **Passed** | [`oj3067-Increment_Decrement ✅`](oj/oj3067-Increment_Decrement%20%E2%9C%85) | [`problem.md`](oj/oj3067-Increment_Decrement%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3067-Increment_Decrement%20%E2%9C%85/main.py) |
| **3068** | ปีอธิกสุรทิน | ✅ **Passed** | [`oj3068-LeapYear ✅`](oj/oj3068-LeapYear%20%E2%9C%85) | [`problem.md`](oj/oj3068-LeapYear%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3068-LeapYear%20%E2%9C%85/main.py) |
| **3069** | ราศี | ✅ **Passed** | [`oj3069-Zodiac ✅`](oj/oj3069-Zodiac%20%E2%9C%85) | [`problem.md`](oj/oj3069-Zodiac%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3069-Zodiac%20%E2%9C%85/main.py) |
| **3070** | นับเลขคู่และเลขคี่ | ✅ **Passed** | [`oj3070-Count_Even_Odd ✅`](oj/oj3070-Count_Even_Odd%20%E2%9C%85) | [`problem.md`](oj/oj3070-Count_Even_Odd%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3070-Count_Even_Odd%20%E2%9C%85/main.py) |

### 📅 Week 4: การทำงานซ้ำแบบ While Loop และตัวแปรสะสม (While Loops & Accumulators)

> รวม `12` ข้อ (ผ่านแล้ว `6/12`)

| OJ ID | Problem Name | Status | Folder Link | Problem Spec | Solution Code |
| :---: | :--- | :---: | :--- | :---: | :---: |
| **3101** | สถานะน้ำ | ✅ **Passed** | [`oj3101-Water_State ✅`](oj/oj3101-Water_State%20%E2%9C%85) | [`problem.md`](oj/oj3101-Water_State%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3101-Water_State%20%E2%9C%85/main.py) |
| **3102** | ภาษีรถยนต์ | ✅ **Passed** | [`oj3102-Car_Tax ✅`](oj/oj3102-Car_Tax%20%E2%9C%85) | [`problem.md`](oj/oj3102-Car_Tax%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3102-Car_Tax%20%E2%9C%85/main.py) |
| **3103** | จำนวนสระ | ✅ **Passed** | [`oj3103-Vowel_Count ✅`](oj/oj3103-Vowel_Count%20%E2%9C%85) | [`problem.md`](oj/oj3103-Vowel_Count%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3103-Vowel_Count%20%E2%9C%85/main.py) |
| **3104** | Ticket | ✅ **Passed** | [`oj3104-Ticket ✅`](oj/oj3104-Ticket%20%E2%9C%85) | [`problem.md`](oj/oj3104-Ticket%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3104-Ticket%20%E2%9C%85/main.py) |
| **3105** | คำนวณค่าแท็กซี่เบื้องต้น | 🔄 *In Progress* | [`oj3105-Taxi_Fare`](oj/oj3105-Taxi_Fare) | [`problem.md`](oj/oj3105-Taxi_Fare/problem.md) | [`main.py`](oj/oj3105-Taxi_Fare/main.py) |
| **3106** | Basic ATM | ✅ **Passed** | [`oj3106-Basic_ATM ✅`](oj/oj3106-Basic_ATM%20%E2%9C%85) | [`problem.md`](oj/oj3106-Basic_ATM%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3106-Basic_ATM%20%E2%9C%85/main.py) |
| **3107** | Bonus | 🔄 *In Progress* | [`oj3107-Bonus`](oj/oj3107-Bonus) | [`problem.md`](oj/oj3107-Bonus/problem.md) | [`main.py`](oj/oj3107-Bonus/main.py) |
| **3108** | คำนวณราคาสินค้าโปรโมชั่น | 🔄 *In Progress* | [`oj3108-Promotion_Price`](oj/oj3108-Promotion_Price) | [`problem.md`](oj/oj3108-Promotion_Price/problem.md) | [`main.py`](oj/oj3108-Promotion_Price/main.py) |
| **3112** | ชานมไข่มุก | 🔄 *In Progress* | [`oj3112-Boba_Tea`](oj/oj3112-Boba_Tea) | [`problem.md`](oj/oj3112-Boba_Tea/problem.md) | [`main.py`](oj/oj3112-Boba_Tea/main.py) |
| **3113** | กระต่ายน้อยกินราเมน | 🔄 *In Progress* | [`oj3113-Ramen_Rabbit`](oj/oj3113-Ramen_Rabbit) | [`problem.md`](oj/oj3113-Ramen_Rabbit/problem.md) | [`main.py`](oj/oj3113-Ramen_Rabbit/main.py) |
| **3114** | Suvarnabhumi Airport Parking | 🔄 *In Progress* | [`oj3114-Suvarnabhumi_Airport_Parking`](oj/oj3114-Suvarnabhumi_Airport_Parking) | [`problem.md`](oj/oj3114-Suvarnabhumi_Airport_Parking/problem.md) | [`main.py`](oj/oj3114-Suvarnabhumi_Airport_Parking/main.py) |
| **3116** | นวัตกรรมงบประมาณโรงเรียน | ✅ **Passed** | [`oj3116-School_Budget_Innovation ✅`](oj/oj3116-School_Budget_Innovation%20%E2%9C%85) | [`problem.md`](oj/oj3116-School_Budget_Innovation%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3116-School_Budget_Innovation%20%E2%9C%85/main.py) |

### 📅 Week 5: การทำงานซ้ำแบบ For Loop และลูปซ้อนลูป (For Loops & Geometry Drawing)

> รวม `12` ข้อ (ผ่านแล้ว `12/12`)

| OJ ID | Problem Name | Status | Folder Link | Problem Spec | Solution Code |
| :---: | :--- | :---: | :--- | :---: | :---: |
| **3129** | วิเคราะห์ยอดขายร้านกาแฟ | ✅ **Passed** | [`oj3129-Coffee_Shop_Sales_Analysis ✅`](oj/oj3129-Coffee_Shop_Sales_Analysis%20%E2%9C%85) | [`problem.md`](oj/oj3129-Coffee_Shop_Sales_Analysis%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3129-Coffee_Shop_Sales_Analysis%20%E2%9C%85/main.py) |
| **3155** | ลูกน้ำ | ✅ **Passed** | [`oj3155-Looknam ✅`](oj/oj3155-Looknam%20%E2%9C%85) | [`problem.md`](oj/oj3155-Looknam%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3155-Looknam%20%E2%9C%85/main.py) |
| **3156** | Conan | ✅ **Passed** | [`oj3156-Conan ✅`](oj/oj3156-Conan%20%E2%9C%85) | [`problem.md`](oj/oj3156-Conan%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3156-Conan%20%E2%9C%85/main.py) |
| **3158** | ผลรวมกำลัง 2 | ✅ **Passed** | [`oj3158-Sum_Of_Squares ✅`](oj/oj3158-Sum_Of_Squares%20%E2%9C%85) | [`problem.md`](oj/oj3158-Sum_Of_Squares%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3158-Sum_Of_Squares%20%E2%9C%85/main.py) |
| **3159** | Factorial | ✅ **Passed** | [`oj3159-Factorial ✅`](oj/oj3159-Factorial%20%E2%9C%85) | [`problem.md`](oj/oj3159-Factorial%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3159-Factorial%20%E2%9C%85/main.py) |
| **3161** | พิมพ์สัญลักษณ์ | ✅ **Passed** | [`oj3161-Print_Symbol ✅`](oj/oj3161-Print_Symbol%20%E2%9C%85) | [`problem.md`](oj/oj3161-Print_Symbol%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3161-Print_Symbol%20%E2%9C%85/main.py) |
| **3162** | ตารางสูตรคูณ | ✅ **Passed** | [`oj3162-Multiplication_Table ✅`](oj/oj3162-Multiplication_Table%20%E2%9C%85) | [`problem.md`](oj/oj3162-Multiplication_Table%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3162-Multiplication_Table%20%E2%9C%85/main.py) |
| **3163** | สินค้าส่งออก | ✅ **Passed** | [`oj3163-Export_Products ✅`](oj/oj3163-Export_Products%20%E2%9C%85) | [`problem.md`](oj/oj3163-Export_Products%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3163-Export_Products%20%E2%9C%85/main.py) |
| **3164** | ผลรวมของค่าที่มากกว่า | ✅ **Passed** | [`oj3164-Sum_Of_Greater_Values ✅`](oj/oj3164-Sum_Of_Greater_Values%20%E2%9C%85) | [`problem.md`](oj/oj3164-Sum_Of_Greater_Values%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3164-Sum_Of_Greater_Values%20%E2%9C%85/main.py) |
| **3165** | เดินเล่นในงานเทศกาล | ✅ **Passed** | [`oj3165-Festival_Walk ✅`](oj/oj3165-Festival_Walk%20%E2%9C%85) | [`problem.md`](oj/oj3165-Festival_Walk%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3165-Festival_Walk%20%E2%9C%85/main.py) |
| **3166** | ผ่านหรือไม่ ค่าเฉลี่ยรายวิชา | ✅ **Passed** | [`oj3166-Course_Average_Pass_Fail ✅`](oj/oj3166-Course_Average_Pass_Fail%20%E2%9C%85) | [`problem.md`](oj/oj3166-Course_Average_Pass_Fail%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3166-Course_Average_Pass_Fail%20%E2%9C%85/main.py) |
| **3167** | FizzBuzz | ✅ **Passed** | [`oj3167-FizzBuzz ✅`](oj/oj3167-FizzBuzz%20%E2%9C%85) | [`problem.md`](oj/oj3167-FizzBuzz%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3167-FizzBuzz%20%E2%9C%85/main.py) |

### 📅 Week 6: ลูปขั้นสูง สตริง และลำดับอนุกรม (Advanced Loops, Strings & Sequences)

> รวม `10` ข้อ (ผ่านแล้ว `10/10`)

| OJ ID | Problem Name | Status | Folder Link | Problem Spec | Solution Code |
| :---: | :--- | :---: | :--- | :---: | :---: |
| **3226** | Inflation | ✅ **Passed** | [`oj3226-Inflation ✅`](oj/oj3226-Inflation%20%E2%9C%85) | [`problem.md`](oj/oj3226-Inflation%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3226-Inflation%20%E2%9C%85/main.py) |
| **3228** | การนับสระ | ✅ **Passed** | [`oj3228-Count_Vowels ✅`](oj/oj3228-Count_Vowels%20%E2%9C%85) | [`problem.md`](oj/oj3228-Count_Vowels%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3228-Count_Vowels%20%E2%9C%85/main.py) |
| **3229** | ระบบคิดคะแนนเกมออนไลน์ | ✅ **Passed** | [`oj3229-Online_Game_Scoring ✅`](oj/oj3229-Online_Game_Scoring%20%E2%9C%85) | [`problem.md`](oj/oj3229-Online_Game_Scoring%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3229-Online_Game_Scoring%20%E2%9C%85/main.py) |
| **3230** | โรงแรมกลางกรุง ไม่มีชั้น 13 | ✅ **Passed** | [`oj3230-Hotel_No_13th_Floor ✅`](oj/oj3230-Hotel_No_13th_Floor%20%E2%9C%85) | [`problem.md`](oj/oj3230-Hotel_No_13th_Floor%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3230-Hotel_No_13th_Floor%20%E2%9C%85/main.py) |
| **3231** | เกมทายลูกเต๋า | ✅ **Passed** | [`oj3231-Dice_Guessing_Game ✅`](oj/oj3231-Dice_Guessing_Game%20%E2%9C%85) | [`problem.md`](oj/oj3231-Dice_Guessing_Game%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3231-Dice_Guessing_Game%20%E2%9C%85/main.py) |
| **3234** | ไฟคริสตมาส | ✅ **Passed** | [`oj3234-Christmas_Lights ✅`](oj/oj3234-Christmas_Lights%20%E2%9C%85) | [`problem.md`](oj/oj3234-Christmas_Lights%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3234-Christmas_Lights%20%E2%9C%85/main.py) |
| **3235** | กระต่ายอ้วน | ✅ **Passed** | [`oj3235-Fat_Rabbit ✅`](oj/oj3235-Fat_Rabbit%20%E2%9C%85) | [`problem.md`](oj/oj3235-Fat_Rabbit%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3235-Fat_Rabbit%20%E2%9C%85/main.py) |
| **3236** | รหัสแฝดเทค | ✅ **Passed** | [`oj3236-Twin_Tech_Code ✅`](oj/oj3236-Twin_Tech_Code%20%E2%9C%85) | [`problem.md`](oj/oj3236-Twin_Tech_Code%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3236-Twin_Tech_Code%20%E2%9C%85/main.py) |
| **3237** | สามเหลี่ยม | ✅ **Passed** | [`oj3237-Triangle ✅`](oj/oj3237-Triangle%20%E2%9C%85) | [`problem.md`](oj/oj3237-Triangle%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3237-Triangle%20%E2%9C%85/main.py) |
| **3238** | Elon Musk (X-shape) | ✅ **Passed** | [`oj3238-Elon_Musk_X_Shape ✅`](oj/oj3238-Elon_Musk_X_Shape%20%E2%9C%85) | [`problem.md`](oj/oj3238-Elon_Musk_X_Shape%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3238-Elon_Musk_X_Shape%20%E2%9C%85/main.py) |

### 📅 Week 7 / Midterm: ชุดข้อสอบจำลองกลางภาค (Midterm Mock Exam)

> รวม `9` ข้อ (ผ่านแล้ว `0/9`)

| OJ ID | Problem Name | Status | Folder Link | Problem Spec | Solution Code |
| :---: | :--- | :---: | :--- | :---: | :---: |
| **3274** | Triangle | 🔄 *In Progress* | [`oj3274-MIDTERM_Triangle`](oj/oj3274-MIDTERM_Triangle) | [`problem.md`](oj/oj3274-MIDTERM_Triangle/problem.md) | [`main.py`](oj/oj3274-MIDTERM_Triangle/main.py) |
| **3275** | PIZZA TIME | 🔄 *In Progress* | [`oj3275-MIDTERM_Pizza_Time`](oj/oj3275-MIDTERM_Pizza_Time) | [`problem.md`](oj/oj3275-MIDTERM_Pizza_Time/problem.md) | [`main.py`](oj/oj3275-MIDTERM_Pizza_Time/main.py) |
| **3276** | FakeThaiPlus | 🔄 *In Progress* | [`oj3276-MIDTERM_FakeThaiPlus`](oj/oj3276-MIDTERM_FakeThaiPlus) | [`problem.md`](oj/oj3276-MIDTERM_FakeThaiPlus/problem.md) | [`main.py`](oj/oj3276-MIDTERM_FakeThaiPlus/main.py) |
| **3277** | RealThaiPlus | 🔄 *In Progress* | [`oj3277-MIDTERM_RealThaiPlus`](oj/oj3277-MIDTERM_RealThaiPlus) | [`problem.md`](oj/oj3277-MIDTERM_RealThaiPlus/problem.md) | [`main.py`](oj/oj3277-MIDTERM_RealThaiPlus/main.py) |
| **3278** | Units | 🔄 *In Progress* | [`oj3278-MIDTERM_Units`](oj/oj3278-MIDTERM_Units) | [`problem.md`](oj/oj3278-MIDTERM_Units/problem.md) | [`main.py`](oj/oj3278-MIDTERM_Units/main.py) |
| **3279** | PM WATCH | 🔄 *In Progress* | [`oj3279-MIDTERM_PM_Watch`](oj/oj3279-MIDTERM_PM_Watch) | [`problem.md`](oj/oj3279-MIDTERM_PM_Watch/problem.md) | [`main.py`](oj/oj3279-MIDTERM_PM_Watch/main.py) |
| **3280** | CODE CLEANER | 🔄 *In Progress* | [`oj3280-MIDTERM_Code_Cleaner`](oj/oj3280-MIDTERM_Code_Cleaner) | [`problem.md`](oj/oj3280-MIDTERM_Code_Cleaner/problem.md) | [`main.py`](oj/oj3280-MIDTERM_Code_Cleaner/main.py) |
| **3281** | ijudge-itkmitl | 🔄 *In Progress* | [`oj3281-MIDTERM_ijudge-itkmitl`](oj/oj3281-MIDTERM_ijudge-itkmitl) | [`problem.md`](oj/oj3281-MIDTERM_ijudge-itkmitl/problem.md) | [`main.py`](oj/oj3281-MIDTERM_ijudge-itkmitl/main.py) |
| **3282** | Stats | 🔄 *In Progress* | [`oj3282-MIDTERM_Stats`](oj/oj3282-MIDTERM_Stats) | [`problem.md`](oj/oj3282-MIDTERM_Stats/problem.md) | [`main.py`](oj/oj3282-MIDTERM_Stats/main.py) |

### 📅 Week 8: ลิสต์และการประมวลผลสตริงขั้นสูง (Lists & Advanced Sequence Operations)

> รวม `9` ข้อ (ผ่านแล้ว `9/9`)

| OJ ID | Problem Name | Status | Folder Link | Problem Spec | Solution Code |
| :---: | :--- | :---: | :--- | :---: | :---: |
| **3290** | Left Arrow | ✅ **Passed** | [`oj3290-Left_Arrow ✅`](oj/oj3290-Left_Arrow%20%E2%9C%85) | [`problem.md`](oj/oj3290-Left_Arrow%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3290-Left_Arrow%20%E2%9C%85/main.py) |
| **3291** | Right Arrow | ✅ **Passed** | [`oj3291-Right_Arrow ✅`](oj/oj3291-Right_Arrow%20%E2%9C%85) | [`problem.md`](oj/oj3291-Right_Arrow%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3291-Right_Arrow%20%E2%9C%85/main.py) |
| **3292** | Arrow | ✅ **Passed** | [`oj3292-Arrow ✅`](oj/oj3292-Arrow%20%E2%9C%85) | [`problem.md`](oj/oj3292-Arrow%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3292-Arrow%20%E2%9C%85/main.py) |
| **3294** | Teaching schedule | ✅ **Passed** | [`oj3294-Teaching_schedule ✅`](oj/oj3294-Teaching_schedule%20%E2%9C%85) | [`problem.md`](oj/oj3294-Teaching_schedule%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3294-Teaching_schedule%20%E2%9C%85/main.py) |
| **3295** | Electric_Using | ✅ **Passed** | [`oj3295-Electric_Using ✅`](oj/oj3295-Electric_Using%20%E2%9C%85) | [`problem.md`](oj/oj3295-Electric_Using%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3295-Electric_Using%20%E2%9C%85/main.py) |
| **3297** | ตั๋วหนังสุดป่วน | ✅ **Passed** | [`oj3297-Movie_Ticket_Trouble ✅`](oj/oj3297-Movie_Ticket_Trouble%20%E2%9C%85) | [`problem.md`](oj/oj3297-Movie_Ticket_Trouble%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3297-Movie_Ticket_Trouble%20%E2%9C%85/main.py) |
| **3298** | กระต่ายน้อยรัก BUU | ✅ **Passed** | [`oj3298-Little_Rabbit_Loves_BUU ✅`](oj/oj3298-Little_Rabbit_Loves_BUU%20%E2%9C%85) | [`problem.md`](oj/oj3298-Little_Rabbit_Loves_BUU%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3298-Little_Rabbit_Loves_BUU%20%E2%9C%85/main.py) |
| **3300** | สมดุลย์ชีวิต | ✅ **Passed** | [`oj3300-Life_Balance ✅`](oj/oj3300-Life_Balance%20%E2%9C%85) | [`problem.md`](oj/oj3300-Life_Balance%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3300-Life_Balance%20%E2%9C%85/main.py) |
| **3301** | ใส่กล่อง | ✅ **Passed** | [`oj3301-Put_In_Box ✅`](oj/oj3301-Put_In_Box%20%E2%9C%85) | [`problem.md`](oj/oj3301-Put_In_Box%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3301-Put_In_Box%20%E2%9C%85/main.py) |

### 📅 Week 9: ลิสต์ขั้นสูงและการประยุกต์ใช้งาน (Advanced Lists & Applied Algorithms)

> รวม `12` ข้อ (ผ่านแล้ว `0/12`)

| OJ ID | Problem Name | Status | Folder Link | Problem Spec | Solution Code |
| :---: | :--- | :---: | :--- | :---: | :---: |
| **3349** | กองชาม | 🔄 *In Progress* | [`oj3349-Bowl_Stack`](oj/oj3349-Bowl_Stack) | [`problem.md`](oj/oj3349-Bowl_Stack/problem.md) | [`main.py`](oj/oj3349-Bowl_Stack/main.py) |
| **3350** | ขายรถยนต์ | 🔄 *In Progress* | [`oj3350-Sell_Car`](oj/oj3350-Sell_Car) | [`problem.md`](oj/oj3350-Sell_Car/problem.md) | [`main.py`](oj/oj3350-Sell_Car/main.py) |
| **3351** | พูดจาภาษากระต่าย | 🔄 *In Progress* | [`oj3351-Rabbit_Language`](oj/oj3351-Rabbit_Language) | [`problem.md`](oj/oj3351-Rabbit_Language/problem.md) | [`main.py`](oj/oj3351-Rabbit_Language/main.py) |
| **3352** | LastStand | 🔄 *In Progress* | [`oj3352-LastStand`](oj/oj3352-LastStand) | [`problem.md`](oj/oj3352-LastStand/problem.md) | [`main.py`](oj/oj3352-LastStand/main.py) |
| **3353** | PickThemAgain | 🔄 *In Progress* | [`oj3353-PickThemAgain`](oj/oj3353-PickThemAgain) | [`problem.md`](oj/oj3353-PickThemAgain/problem.md) | [`main.py`](oj/oj3353-PickThemAgain/main.py) |
| **3354** | Hint | 🔄 *In Progress* | [`oj3354-Hint`](oj/oj3354-Hint) | [`problem.md`](oj/oj3354-Hint/problem.md) | [`main.py`](oj/oj3354-Hint/main.py) |
| **3356** | Bus Seat | 🔄 *In Progress* | [`oj3356-Bus_Seat`](oj/oj3356-Bus_Seat) | [`problem.md`](oj/oj3356-Bus_Seat/problem.md) | [`main.py`](oj/oj3356-Bus_Seat/main.py) |
| **3358** | Pig | 🔄 *In Progress* | [`oj3358-Pig`](oj/oj3358-Pig) | [`problem.md`](oj/oj3358-Pig/problem.md) | [`main.py`](oj/oj3358-Pig/main.py) |
| **3359** | กองชาม | 🔄 *In Progress* | [`oj3359-Bowl_Stack_II`](oj/oj3359-Bowl_Stack_II) | [`problem.md`](oj/oj3359-Bowl_Stack_II/problem.md) | [`main.py`](oj/oj3359-Bowl_Stack_II/main.py) |
| **3361** | ขายรถยนต์ | 🔄 *In Progress* | [`oj3361-Sell_Car_II`](oj/oj3361-Sell_Car_II) | [`problem.md`](oj/oj3361-Sell_Car_II/problem.md) | [`main.py`](oj/oj3361-Sell_Car_II/main.py) |
| **3362** | บุพเพสันนิวาส | 🔄 *In Progress* | [`oj3362-Destiny_Love`](oj/oj3362-Destiny_Love) | [`problem.md`](oj/oj3362-Destiny_Love/problem.md) | [`main.py`](oj/oj3362-Destiny_Love/main.py) |
| **3363** | ไข้หวัดกระต่ายสายพันธุ์ใหม่ | 🔄 *In Progress* | [`oj3363-New_Rabbit_Flu_Strain`](oj/oj3363-New_Rabbit_Flu_Strain) | [`problem.md`](oj/oj3363-New_Rabbit_Flu_Strain/problem.md) | [`main.py`](oj/oj3363-New_Rabbit_Flu_Strain/main.py) |

### 📅 Week 10: ทูเพิล ลิสต์ 2 มิติ และการเรียงลำดับ (Tuples, 2D Lists & Sorting)

> รวม `13` ข้อ (ผ่านแล้ว `0/13`)

| OJ ID | Problem Name | Status | Folder Link | Problem Spec | Solution Code |
| :---: | :--- | :---: | :--- | :---: | :---: |
| **3382** | Day08-0_02-Backward | 🔄 *In Progress* | [`oj3382-Day08-0_02-Backward`](oj/oj3382-Day08-0_02-Backward) | [`problem.md`](oj/oj3382-Day08-0_02-Backward/problem.md) | [`main.py`](oj/oj3382-Day08-0_02-Backward/main.py) |
| **3383** | Difference | 🔄 *In Progress* | [`oj3383-Difference`](oj/oj3383-Difference) | [`problem.md`](oj/oj3383-Difference/problem.md) | [`main.py`](oj/oj3383-Difference/main.py) |
| **3384** | PickThem | 🔄 *In Progress* | [`oj3384-PickThem`](oj/oj3384-PickThem) | [`problem.md`](oj/oj3384-PickThem/problem.md) | [`main.py`](oj/oj3384-PickThem/main.py) |
| **3385** | BusStop I | 🔄 *In Progress* | [`oj3385-BusStop_I`](oj/oj3385-BusStop_I) | [`problem.md`](oj/oj3385-BusStop_I/problem.md) | [`main.py`](oj/oj3385-BusStop_I/main.py) |
| **3387** | Tuple's Sad life | 🔄 *In Progress* | [`oj3387-Tuples_Sad_life`](oj/oj3387-Tuples_Sad_life) | [`problem.md`](oj/oj3387-Tuples_Sad_life/problem.md) | [`main.py`](oj/oj3387-Tuples_Sad_life/main.py) |
| **3388** | 113 | 🔄 *In Progress* | [`oj3388-113`](oj/oj3388-113) | [`problem.md`](oj/oj3388-113/problem.md) | [`main.py`](oj/oj3388-113/main.py) |
| **3389** | Smart Trash Collector | 🔄 *In Progress* | [`oj3389-Smart_Trash_Collector`](oj/oj3389-Smart_Trash_Collector) | [`problem.md`](oj/oj3389-Smart_Trash_Collector/problem.md) | [`main.py`](oj/oj3389-Smart_Trash_Collector/main.py) |
| **3390** | Array 2D ตรวจสอบ | 🔄 *In Progress* | [`oj3390-Array_2D_Check`](oj/oj3390-Array_2D_Check) | [`problem.md`](oj/oj3390-Array_2D_Check/problem.md) | [`main.py`](oj/oj3390-Array_2D_Check/main.py) |
| **3391** | สะสมเหรียญเวทย์มนตร์ | 🔄 *In Progress* | [`oj3391-Magic_Coin_Collection`](oj/oj3391-Magic_Coin_Collection) | [`problem.md`](oj/oj3391-Magic_Coin_Collection/problem.md) | [`main.py`](oj/oj3391-Magic_Coin_Collection/main.py) |
| **3392** | Array ฮาเฮ | 🔄 *In Progress* | [`oj3392-Array_Haha`](oj/oj3392-Array_Haha) | [`problem.md`](oj/oj3392-Array_Haha/problem.md) | [`main.py`](oj/oj3392-Array_Haha/main.py) |
| **3393** | นักสำรวจถ้ำ (Cave Explorer) | 🔄 *In Progress* | [`oj3393-Cave_Explorer`](oj/oj3393-Cave_Explorer) | [`problem.md`](oj/oj3393-Cave_Explorer/problem.md) | [`main.py`](oj/oj3393-Cave_Explorer/main.py) |
| **3395** | เข้าแถว | 🔄 *In Progress* | [`oj3395-Line_Up`](oj/oj3395-Line_Up) | [`problem.md`](oj/oj3395-Line_Up/problem.md) | [`main.py`](oj/oj3395-Line_Up/main.py) |
| **3396** | แซงรอบ | 🔄 *In Progress* | [`oj3396-Lap_Overtake`](oj/oj3396-Lap_Overtake) | [`problem.md`](oj/oj3396-Lap_Overtake/problem.md) | [`main.py`](oj/oj3396-Lap_Overtake/main.py) |

### 📅 Week 11: การจำลองการทำงานและเซต (Simulation, String Processing & Sets)

> รวม `13` ข้อ (ผ่านแล้ว `0/13`)

| OJ ID | Problem Name | Status | Folder Link | Problem Spec | Solution Code |
| :---: | :--- | :---: | :--- | :---: | :---: |
| **3473** | FourDirections | 🔄 *In Progress* | [`oj3473-FourDirections`](oj/oj3473-FourDirections) | [`problem.md`](oj/oj3473-FourDirections/problem.md) | [`main.py`](oj/oj3473-FourDirections/main.py) |
| **3474** | Resistor | 🔄 *In Progress* | [`oj3474-Resistor`](oj/oj3474-Resistor) | [`problem.md`](oj/oj3474-Resistor/problem.md) | [`main.py`](oj/oj3474-Resistor/main.py) |
| **3475** | Muddled Menu | 🔄 *In Progress* | [`oj3475-Muddled_Menu`](oj/oj3475-Muddled_Menu) | [`problem.md`](oj/oj3475-Muddled_Menu/problem.md) | [`main.py`](oj/oj3475-Muddled_Menu/main.py) |
| **3478** | Easy Histogram No Dict | 🔄 *In Progress* | [`oj3478-Easy_Histogram_No_Dict`](oj/oj3478-Easy_Histogram_No_Dict) | [`problem.md`](oj/oj3478-Easy_Histogram_No_Dict/problem.md) | [`main.py`](oj/oj3478-Easy_Histogram_No_Dict/main.py) |
| **3479** | Name of Card | 🔄 *In Progress* | [`oj3479-Name_of_Card`](oj/oj3479-Name_of_Card) | [`problem.md`](oj/oj3479-Name_of_Card/problem.md) | [`main.py`](oj/oj3479-Name_of_Card/main.py) |
| **3480** | นก | 🔄 *In Progress* | [`oj3480-Bird`](oj/oj3480-Bird) | [`problem.md`](oj/oj3480-Bird/problem.md) | [`main.py`](oj/oj3480-Bird/main.py) |
| **3481** | ลอดสะพาน | 🔄 *In Progress* | [`oj3481-Under_The_Bridge`](oj/oj3481-Under_The_Bridge) | [`problem.md`](oj/oj3481-Under_The_Bridge/problem.md) | [`main.py`](oj/oj3481-Under_The_Bridge/main.py) |
| **3482** | นักล่าอสูร | 🔄 *In Progress* | [`oj3482-Demon_Slayer`](oj/oj3482-Demon_Slayer) | [`problem.md`](oj/oj3482-Demon_Slayer/problem.md) | [`main.py`](oj/oj3482-Demon_Slayer/main.py) |
| **3483** | มาเป็นทีม | 🔄 *In Progress* | [`oj3483-Team_Up`](oj/oj3483-Team_Up) | [`problem.md`](oj/oj3483-Team_Up/problem.md) | [`main.py`](oj/oj3483-Team_Up/main.py) |
| **3485** | รหัสต้องไม่ซ้ำกัน | 🔄 *In Progress* | [`oj3485-Unique_Code`](oj/oj3485-Unique_Code) | [`problem.md`](oj/oj3485-Unique_Code/problem.md) | [`main.py`](oj/oj3485-Unique_Code/main.py) |
| **3486** | ตำบลกระสุนตก | 🔄 *In Progress* | [`oj3486-Artillery_Impact`](oj/oj3486-Artillery_Impact) | [`problem.md`](oj/oj3486-Artillery_Impact/problem.md) | [`main.py`](oj/oj3486-Artillery_Impact/main.py) |
| **3487** | ติดตั้งหลอดไฟ | 🔄 *In Progress* | [`oj3487-Install_Light`](oj/oj3487-Install_Light) | [`problem.md`](oj/oj3487-Install_Light/problem.md) | [`main.py`](oj/oj3487-Install_Light/main.py) |
| **3488** | ไฟส่อง | 🔄 *In Progress* | [`oj3488-Spotlight`](oj/oj3488-Spotlight) | [`problem.md`](oj/oj3488-Spotlight/problem.md) | [`main.py`](oj/oj3488-Spotlight/main.py) |

### 📅 Week 12: ดิกชันนารีและเซตขั้นสูง (Advanced Dictionaries, Sets & Algorithms)

> รวม `13` ข้อ (ผ่านแล้ว `0/13`)

| OJ ID | Problem Name | Status | Folder Link | Problem Spec | Solution Code |
| :---: | :--- | :---: | :--- | :---: | :---: |
| **3529** | CaesarV2 | 🔄 *In Progress* | [`oj3529-CaesarV2`](oj/oj3529-CaesarV2) | [`problem.md`](oj/oj3529-CaesarV2/problem.md) | [`main.py`](oj/oj3529-CaesarV2/main.py) |
| **3530** | SqFree | 🔄 *In Progress* | [`oj3530-SqFree`](oj/oj3530-SqFree) | [`problem.md`](oj/oj3530-SqFree/problem.md) | [`main.py`](oj/oj3530-SqFree/main.py) |
| **3531** | MissingNumber | 🔄 *In Progress* | [`oj3531-MissingNumber`](oj/oj3531-MissingNumber) | [`problem.md`](oj/oj3531-MissingNumber/problem.md) | [`main.py`](oj/oj3531-MissingNumber/main.py) |
| **3532** | GCD_v2 | 🔄 *In Progress* | [`oj3532-GCD_v2`](oj/oj3532-GCD_v2) | [`problem.md`](oj/oj3532-GCD_v2/problem.md) | [`main.py`](oj/oj3532-GCD_v2/main.py) |
| **3533** | HorizontalHistogram | 🔄 *In Progress* | [`oj3533-HorizontalHistogram`](oj/oj3533-HorizontalHistogram) | [`problem.md`](oj/oj3533-HorizontalHistogram/problem.md) | [`main.py`](oj/oj3533-HorizontalHistogram/main.py) |
| **3534** | Filter | 🔄 *In Progress* | [`oj3534-Filter`](oj/oj3534-Filter) | [`problem.md`](oj/oj3534-Filter/problem.md) | [`main.py`](oj/oj3534-Filter/main.py) |
| **3535** | Classify | 🔄 *In Progress* | [`oj3535-Classify`](oj/oj3535-Classify) | [`problem.md`](oj/oj3535-Classify/problem.md) | [`main.py`](oj/oj3535-Classify/main.py) |
| **3539** | iPhone 13 Again | 🔄 *In Progress* | [`oj3539-iPhone_13_Again`](oj/oj3539-iPhone_13_Again) | [`problem.md`](oj/oj3539-iPhone_13_Again/problem.md) | [`main.py`](oj/oj3539-iPhone_13_Again/main.py) |
| **3540** | DigitV3 | 🔄 *In Progress* | [`oj3540-DigitV3`](oj/oj3540-DigitV3) | [`problem.md`](oj/oj3540-DigitV3/problem.md) | [`main.py`](oj/oj3540-DigitV3/main.py) |
| **3541** | Coke V2 | 🔄 *In Progress* | [`oj3541-Coke_V2`](oj/oj3541-Coke_V2) | [`problem.md`](oj/oj3541-Coke_V2/problem.md) | [`main.py`](oj/oj3541-Coke_V2/main.py) |
| **3542** | Calculator V2 | 🔄 *In Progress* | [`oj3542-Calculator_V2`](oj/oj3542-Calculator_V2) | [`problem.md`](oj/oj3542-Calculator_V2/problem.md) | [`main.py`](oj/oj3542-Calculator_V2/main.py) |
| **3543** | ช่วย List Prime (Sieve of Eratosthenes) | 🔄 *In Progress* | [`oj3543-Sieve_of_Eratosthenes`](oj/oj3543-Sieve_of_Eratosthenes) | [`problem.md`](oj/oj3543-Sieve_of_Eratosthenes/problem.md) | [`main.py`](oj/oj3543-Sieve_of_Eratosthenes/main.py) |
| **3544** | ระบบจัดการคลังสินค้า | 🔄 *In Progress* | [`oj3544-Warehouse_Management`](oj/oj3544-Warehouse_Management) | [`problem.md`](oj/oj3544-Warehouse_Management/problem.md) | [`main.py`](oj/oj3544-Warehouse_Management/main.py) |

### 📅 Week 13: การเรียกซ้ำ (Recursion & Divide and Conquer)

> รวม `13` ข้อ (ผ่านแล้ว `2/13`)

| OJ ID | Problem Name | Status | Folder Link | Problem Spec | Solution Code |
| :---: | :--- | :---: | :--- | :---: | :---: |
| **3586** | Kabata | 🔄 *In Progress* | [`oj3586-Kabata`](oj/oj3586-Kabata) | [`problem.md`](oj/oj3586-Kabata/problem.md) | [`main.py`](oj/oj3586-Kabata/main.py) |
| **3587** | OneTwo | 🔄 *In Progress* | [`oj3587-OneTwo`](oj/oj3587-OneTwo) | [`problem.md`](oj/oj3587-OneTwo/problem.md) | [`main.py`](oj/oj3587-OneTwo/main.py) |
| **3588** | GCD_N | ✅ **Passed** | [`oj3588-GCD_N ✅`](oj/oj3588-GCD_N%20%E2%9C%85) | [`problem.md`](oj/oj3588-GCD_N%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3588-GCD_N%20%E2%9C%85/main.py) |
| **3589** | FibonacciRecursionV1 | 🔄 *In Progress* | [`oj3589-FibonacciRecursionV1`](oj/oj3589-FibonacciRecursionV1) | [`problem.md`](oj/oj3589-FibonacciRecursionV1/problem.md) | [`main.py`](oj/oj3589-FibonacciRecursionV1/main.py) |
| **3590** | Flatten | 🔄 *In Progress* | [`oj3590-Flatten`](oj/oj3590-Flatten) | [`problem.md`](oj/oj3590-Flatten/problem.md) | [`main.py`](oj/oj3590-Flatten/main.py) |
| **3591** | Olympic | 🔄 *In Progress* | [`oj3591-Olympic`](oj/oj3591-Olympic) | [`problem.md`](oj/oj3591-Olympic/problem.md) | [`main.py`](oj/oj3591-Olympic/main.py) |
| **3592** | Align | ✅ **Passed** | [`oj3592-Align ✅`](oj/oj3592-Align%20%E2%9C%85) | [`problem.md`](oj/oj3592-Align%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3592-Align%20%E2%9C%85/main.py) |
| **3593** | FibonacciRecursionV2 | 🔄 *In Progress* | [`oj3593-FibonacciRecursionV2`](oj/oj3593-FibonacciRecursionV2) | [`problem.md`](oj/oj3593-FibonacciRecursionV2/problem.md) | [`main.py`](oj/oj3593-FibonacciRecursionV2/main.py) |
| **3594** | 1132-Median | 🔄 *In Progress* | [`oj3594-1132-Median`](oj/oj3594-1132-Median) | [`problem.md`](oj/oj3594-1132-Median/problem.md) | [`main.py`](oj/oj3594-1132-Median/main.py) |
| **3595** | Meteorite | 🔄 *In Progress* | [`oj3595-Meteorite`](oj/oj3595-Meteorite) | [`problem.md`](oj/oj3595-Meteorite/problem.md) | [`main.py`](oj/oj3595-Meteorite/main.py) |
| **3596** | Ramen Bowl | 🔄 *In Progress* | [`oj3596-Ramen_Bowl`](oj/oj3596-Ramen_Bowl) | [`problem.md`](oj/oj3596-Ramen_Bowl/problem.md) | [`main.py`](oj/oj3596-Ramen_Bowl/main.py) |
| **3597** | Paper Cut | 🔄 *In Progress* | [`oj3597-Paper_Cut`](oj/oj3597-Paper_Cut) | [`problem.md`](oj/oj3597-Paper_Cut/problem.md) | [`main.py`](oj/oj3597-Paper_Cut/main.py) |
| **3598** | สถิติคลื่นความร้อน | 🔄 *In Progress* | [`oj3598-Heatwave_Statistics`](oj/oj3598-Heatwave_Statistics) | [`problem.md`](oj/oj3598-Heatwave_Statistics/problem.md) | [`main.py`](oj/oj3598-Heatwave_Statistics/main.py) |

### 📅 Week 14: ชุดข้อสอบย่อยจำลอง (Mini Exam / Mock Test)

> รวม `28` ข้อ (ผ่านแล้ว `2/28`)

| OJ ID | Problem Name | Status | Folder Link | Problem Spec | Solution Code |
| :---: | :--- | :---: | :--- | :---: | :---: |
| **3489** | Divide3Or5 | 🔄 *In Progress* | [`oj3489-MINI_EXAM_Divide3Or5`](oj/oj3489-MINI_EXAM_Divide3Or5) | [`problem.md`](oj/oj3489-MINI_EXAM_Divide3Or5/problem.md) | [`main.py`](oj/oj3489-MINI_EXAM_Divide3Or5/main.py) |
| **3490** | Virus I | 🔄 *In Progress* | [`oj3490-MINI_EXAM_Virus_I`](oj/oj3490-MINI_EXAM_Virus_I) | [`problem.md`](oj/oj3490-MINI_EXAM_Virus_I/problem.md) | [`main.py`](oj/oj3490-MINI_EXAM_Virus_I/main.py) |
| **3491** | RunGame | 🔄 *In Progress* | [`oj3491-MINI_EXAM_RunGame`](oj/oj3491-MINI_EXAM_RunGame) | [`problem.md`](oj/oj3491-MINI_EXAM_RunGame/problem.md) | [`main.py`](oj/oj3491-MINI_EXAM_RunGame/main.py) |
| **3492** | Longer | 🔄 *In Progress* | [`oj3492-MINI_EXAM_Longer`](oj/oj3492-MINI_EXAM_Longer) | [`problem.md`](oj/oj3492-MINI_EXAM_Longer/problem.md) | [`main.py`](oj/oj3492-MINI_EXAM_Longer/main.py) |
| **3494** | Nearer | 🔄 *In Progress* | [`oj3494-MINI_EXAM_Nearer`](oj/oj3494-MINI_EXAM_Nearer) | [`problem.md`](oj/oj3494-MINI_EXAM_Nearer/problem.md) | [`main.py`](oj/oj3494-MINI_EXAM_Nearer/main.py) |
| **3495** | Squid Game 3 - Tug-of-War | 🔄 *In Progress* | [`oj3495-MINI_EXAM_Squid_Game_3_-_Tug-of-War`](oj/oj3495-MINI_EXAM_Squid_Game_3_-_Tug-of-War) | [`problem.md`](oj/oj3495-MINI_EXAM_Squid_Game_3_-_Tug-of-War/problem.md) | [`main.py`](oj/oj3495-MINI_EXAM_Squid_Game_3_-_Tug-of-War/main.py) |
| **3496** | A+B Upgrade | 🔄 *In Progress* | [`oj3496-MINI_EXAM_AB_Upgrade`](oj/oj3496-MINI_EXAM_AB_Upgrade) | [`problem.md`](oj/oj3496-MINI_EXAM_AB_Upgrade/problem.md) | [`main.py`](oj/oj3496-MINI_EXAM_AB_Upgrade/main.py) |
| **3497** | Count All Vowel | 🔄 *In Progress* | [`oj3497-MINI_EXAM_Count_All_Vowel`](oj/oj3497-MINI_EXAM_Count_All_Vowel) | [`problem.md`](oj/oj3497-MINI_EXAM_Count_All_Vowel/problem.md) | [`main.py`](oj/oj3497-MINI_EXAM_Count_All_Vowel/main.py) |
| **3499** | Noodle | 🔄 *In Progress* | [`oj3499-MINI_EXAM_Noodle`](oj/oj3499-MINI_EXAM_Noodle) | [`problem.md`](oj/oj3499-MINI_EXAM_Noodle/problem.md) | [`main.py`](oj/oj3499-MINI_EXAM_Noodle/main.py) |
| **3500** | Sairahat | 🔄 *In Progress* | [`oj3500-MINI_EXAM_Sairahat`](oj/oj3500-MINI_EXAM_Sairahat) | [`problem.md`](oj/oj3500-MINI_EXAM_Sairahat/problem.md) | [`main.py`](oj/oj3500-MINI_EXAM_Sairahat/main.py) |
| **3501** | GG-EZ | 🔄 *In Progress* | [`oj3501-MINI_EXAM_GG-EZ`](oj/oj3501-MINI_EXAM_GG-EZ) | [`problem.md`](oj/oj3501-MINI_EXAM_GG-EZ/problem.md) | [`main.py`](oj/oj3501-MINI_EXAM_GG-EZ/main.py) |
| **3502** | Calendar | 🔄 *In Progress* | [`oj3502-MINI_EXAM_Calendar`](oj/oj3502-MINI_EXAM_Calendar) | [`problem.md`](oj/oj3502-MINI_EXAM_Calendar/problem.md) | [`main.py`](oj/oj3502-MINI_EXAM_Calendar/main.py) |
| **3504** | Hamming | 🔄 *In Progress* | [`oj3504-MINI_EXAM_Hamming`](oj/oj3504-MINI_EXAM_Hamming) | [`problem.md`](oj/oj3504-MINI_EXAM_Hamming/problem.md) | [`main.py`](oj/oj3504-MINI_EXAM_Hamming/main.py) |
| **3505** | PickNum | 🔄 *In Progress* | [`oj3505-MINI_EXAM_PickNum`](oj/oj3505-MINI_EXAM_PickNum) | [`problem.md`](oj/oj3505-MINI_EXAM_PickNum/problem.md) | [`main.py`](oj/oj3505-MINI_EXAM_PickNum/main.py) |
| **3506** | WordSequence I | 🔄 *In Progress* | [`oj3506-MINI_EXAM_WordSequence_I`](oj/oj3506-MINI_EXAM_WordSequence_I) | [`problem.md`](oj/oj3506-MINI_EXAM_WordSequence_I/problem.md) | [`main.py`](oj/oj3506-MINI_EXAM_WordSequence_I/main.py) |
| **3507** | Divide3Or5 | 🔄 *In Progress* | [`oj3507-MINI_EXAM_Divide3Or5`](oj/oj3507-MINI_EXAM_Divide3Or5) | [`problem.md`](oj/oj3507-MINI_EXAM_Divide3Or5/problem.md) | [`main.py`](oj/oj3507-MINI_EXAM_Divide3Or5/main.py) |
| **3508** | Virus I | 🔄 *In Progress* | [`oj3508-MINI_EXAM_Virus_I`](oj/oj3508-MINI_EXAM_Virus_I) | [`problem.md`](oj/oj3508-MINI_EXAM_Virus_I/problem.md) | [`main.py`](oj/oj3508-MINI_EXAM_Virus_I/main.py) |
| **3509** | Longer | 🔄 *In Progress* | [`oj3509-MINI_EXAM_Longer`](oj/oj3509-MINI_EXAM_Longer) | [`problem.md`](oj/oj3509-MINI_EXAM_Longer/problem.md) | [`main.py`](oj/oj3509-MINI_EXAM_Longer/main.py) |
| **3510** | Professor | 🔄 *In Progress* | [`oj3510-MINI_EXAM_Professor`](oj/oj3510-MINI_EXAM_Professor) | [`problem.md`](oj/oj3510-MINI_EXAM_Professor/problem.md) | [`main.py`](oj/oj3510-MINI_EXAM_Professor/main.py) |
| **3511** | Rain | 🔄 *In Progress* | [`oj3511-MINI_EXAM_Rain`](oj/oj3511-MINI_EXAM_Rain) | [`problem.md`](oj/oj3511-MINI_EXAM_Rain/problem.md) | [`main.py`](oj/oj3511-MINI_EXAM_Rain/main.py) |
| **3546** | Dart | 🔄 *In Progress* | [`oj3546-MINI_EXAM_Dart`](oj/oj3546-MINI_EXAM_Dart) | [`problem.md`](oj/oj3546-MINI_EXAM_Dart/problem.md) | [`main.py`](oj/oj3546-MINI_EXAM_Dart/main.py) |
| **3547** | Cat in the Bag | 🔄 *In Progress* | [`oj3547-MINI_EXAM_Cat_in_the_Bag`](oj/oj3547-MINI_EXAM_Cat_in_the_Bag) | [`problem.md`](oj/oj3547-MINI_EXAM_Cat_in_the_Bag/problem.md) | [`main.py`](oj/oj3547-MINI_EXAM_Cat_in_the_Bag/main.py) |
| **3548** | Item checker | 🔄 *In Progress* | [`oj3548-MINI_EXAM_Item_checker`](oj/oj3548-MINI_EXAM_Item_checker) | [`problem.md`](oj/oj3548-MINI_EXAM_Item_checker/problem.md) | [`main.py`](oj/oj3548-MINI_EXAM_Item_checker/main.py) |
| **3549** | Book shelf | 🔄 *In Progress* | [`oj3549-MINI_EXAM_Book_shelf`](oj/oj3549-MINI_EXAM_Book_shelf) | [`problem.md`](oj/oj3549-MINI_EXAM_Book_shelf/problem.md) | [`main.py`](oj/oj3549-MINI_EXAM_Book_shelf/main.py) |
| **3550** | Sorry | 🔄 *In Progress* | [`oj3550-MINI_EXAM_Sorry`](oj/oj3550-MINI_EXAM_Sorry) | [`problem.md`](oj/oj3550-MINI_EXAM_Sorry/problem.md) | [`main.py`](oj/oj3550-MINI_EXAM_Sorry/main.py) |
| **3551** | Adventurer's Backpack | 🔄 *In Progress* | [`oj3551-MINI_EXAM_Adventurers_Backpack`](oj/oj3551-MINI_EXAM_Adventurers_Backpack) | [`problem.md`](oj/oj3551-MINI_EXAM_Adventurers_Backpack/problem.md) | [`main.py`](oj/oj3551-MINI_EXAM_Adventurers_Backpack/main.py) |
| **3599** | SumOfNumber | ✅ **Passed** | [`oj3599-SumOfNumber ✅`](oj/oj3599-SumOfNumber%20%E2%9C%85) | [`problem.md`](oj/oj3599-SumOfNumber%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3599-SumOfNumber%20%E2%9C%85/main.py) |
| **3600** | แคลอรี่ | ✅ **Passed** | [`oj3600-Calories ✅`](oj/oj3600-Calories%20%E2%9C%85) | [`problem.md`](oj/oj3600-Calories%20%E2%9C%85/problem.md) | [`main.py`](oj/oj3600-Calories%20%E2%9C%85/main.py) |

---

## 🛠️ Data & Automation Scripts

ไฟล์ทั้งหมดในหัวข้อนี้อยู่บน branch `OP` (worktree `.op/`) ไม่ใช่ `main`

- [`data/course.json`](https://github.com/Jesselpetry/pscp-69070027/blob/OP/data/course.json) — Course config: week windows (release dates), week titles, category tags, folder names, midterm map. Adding a week = one entry here.
- [`data/oj_problems.json`](https://github.com/Jesselpetry/pscp-69070027/blob/OP/data/oj_problems.json) — Summary registry (224 problems): id, week, status, pass stats, deadline, release date, and category flags.
- [`data/all_problems_detail.json`](https://github.com/Jesselpetry/pscp-69070027/blob/OP/data/all_problems_detail.json) — Detail registry (223 problems): problem statements, input/output specifications, time/memory limits, and sample testcases.
- [`solutions/`](https://github.com/Jesselpetry/pscp-69070027/tree/OP/solutions) — Archived reference code (224 problems): `solutions/oj<id>/main.py`.
- [`scripts/pscp.py`](https://github.com/Jesselpetry/pscp-69070027/blob/OP/scripts/pscp.py) — Single entry point: `python3 .op/scripts/pscp.py <command>` runs every script below.
- [`scripts/scrape_all_oj_problems.py`](https://github.com/Jesselpetry/pscp-69070027/blob/OP/scripts/scrape_all_oj_problems.py) — iJudge scraper: summary + detail registries, with a React Server Component (RSC) stream resolver.
- [`scripts/render_problems.py`](https://github.com/Jesselpetry/pscp-69070027/blob/OP/scripts/render_problems.py) — Registry → `problem.md` for every problem + `main.py` stubs for new ones (offline, idempotent).
- [`scripts/update_readme.py`](https://github.com/Jesselpetry/pscp-69070027/blob/OP/scripts/update_readme.py) — Generates this README.md (only the README). Edit the script, not the README: manual edits are overwritten.
- [`scripts/sync_oj_status.py`](https://github.com/Jesselpetry/pscp-69070027/blob/OP/scripts/sync_oj_status.py) — Renames `oj/` folders to match the pass status (` ✅` suffix).
- [`scripts/check_repo.py`](https://github.com/Jesselpetry/pscp-69070027/blob/OP/scripts/check_repo.py) — Read-only consistency check (`doctor`): registry ↔ folders, weeks, Learning Logs, archived solutions.
- [`scripts/archive_solutions.py`](https://github.com/Jesselpetry/pscp-69070027/blob/OP/scripts/archive_solutions.py) — Copies solved `main.py` files from main into `solutions/` on the OP branch.
- [`scripts/run_samples.py`](https://github.com/Jesselpetry/pscp-69070027/blob/OP/scripts/run_samples.py) — Runs a problem's `main.py` against the official sample testcases.
- [`scripts/submit_oj.py`](https://github.com/Jesselpetry/pscp-69070027/blob/OP/scripts/submit_oj.py) — Submission CLI with session-cookie management and result polling.
- [`scripts/README.md`](https://github.com/Jesselpetry/pscp-69070027/blob/OP/scripts/README.md) — Setup, credentials, and every command option.

### 🔁 Weekly Workflow

```bash
python3 .op/scripts/pscp.py scrape --fast         # refresh the problem list and status
python3 .op/scripts/pscp.py scrape --only <ids>   # fetch details of new problems
python3 .op/scripts/pscp.py render                # problem.md + main.py stubs on main
python3 .op/scripts/pscp.py test <id>             # run main.py against the official samples
python3 .op/scripts/pscp.py archive               # copy solved main.py into solutions/ (OP)
python3 .op/scripts/pscp.py readme                # regenerate this README
python3 .op/scripts/pscp.py doctor                # check that nothing is out of sync
```

### 🗺️ Roadmap

แผนจัดระเบียบ repo และขั้นตอนแต่ละ phase อยู่ที่ [`docs/PLAN.md`](https://github.com/Jesselpetry/pscp-69070027/blob/OP/docs/PLAN.md) บน branch `OP`

---

## 🐍 Code Style Guidelines

All Python solutions follow strict PEP-8 standards with docstrings:

```python
""" Problem Name """


def main():
    """Problem Name"""
    # solution code here


if __name__ == "__main__":
    main()
```
