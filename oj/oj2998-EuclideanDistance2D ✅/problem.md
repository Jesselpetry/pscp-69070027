# OJ 2998: EuclideanDistance2D

> - **iJudge cp_id**: 2998 — ภาษา Python
> - **เวลาจำกัด**: 1 วินาที | **หน่วยความจำ**: 32,000 KB

---

## 1. โจทย์จริงจาก iJudge

จงเขียนโปรแกรมรับตัวเลข 4 ตัวจากผู้ใช้ตามลำดับ <em>q1</em>, <em>q2</em>, <em>p1</em>, <em>p2</em>
กำหนดให้&nbsp;ในระนาบ 2 มิติ จุด <strong>Q</strong> อยู่ที่ตำแหน่ง (<em>q1</em>, <em>q2</em>)&nbsp; และจุด <strong>P</strong> อยู่ที่ตำแหน่ง&nbsp;(<em>p1</em>, <em>p2</em>)<br />
จงหาระยะทางแบบยุคลิค (Euclidean distance) ระหว่างจุด <strong>Q</strong> และ <strong>P</strong>
โดย&nbsp;ระยะทางแบบยุคลิคระหว่าง <strong>Q</strong> และ <strong>P</strong> ใดๆ ในระนาบ <em>n</em> มิติ มีค่าเท่ากับ
<br />
<div style="text-align: center;"><img alt="{\displaystyle {\begin{aligned}d(\mathbf {p} ,\mathbf {q} )=d(\mathbf {q} ,\mathbf {p} )&amp;={\sqrt {(q_{1}-p_{1})^{2}+(q_{2}-p_{2})^{2}+\cdots +(q_{n}-p_{n})^{2}}}\\[8pt]&amp;={\sqrt {\sum _{i=1}^{n}(q_{i}-p_{i})^{2}}}.\end{aligned}}}" src="https://i.sstatic.net/RtnTY.jpg" /></div>

## 2. Input Specification

**<u>4 บรรทัด</u>**

**บรรทัดที่ 1:** ค่า q1
**บรรทัดที่ 2:** ค่า q2
**บรรทัดที่ 3:** ค่า p1
**บรรทัดที่ 4:** ค่า p2

ทั้งหมดเป็น <b>จำนวนจริง</b>

## 3. Output Specification

**<u>1 บรรทัด</u>**

**บรรทัดที่ 1:** `ระยะทางแบบยุคลิคระหว่างจุด Q และ P`

**เป็นจำนวนจริง**

## 4. ตัวอย่างจาก iJudge

### ตัวอย่างที่ 1
- **อินพุต**:
  ```text
  1
  1
  2
  2
  ```
- **เอาต์พุต**:
  ```text
  1.4142135623730951
  ```

### ตัวอย่างที่ 2
- **อินพุต**:
  ```text
  2.05
  -3
  1.69
  0
  ```
- **เอาต์พุต**:
  ```text
  3.0215227948834014
  ```
