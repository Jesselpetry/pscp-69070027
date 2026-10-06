# OJ 3594: 1132-Median

> - **iJudge cp_id**: 3594 — ภาษา Python
> - **เวลาจำกัด**: 1 วินาที | **หน่วยความจำ**: 32,768 KB

---

## 1. โจทย์จริงจาก iJudge

<span style="color:#000000"><span style="font-size:16px"><span style="font-family:arial,helvetica,sans-serif">ค่ามัธยฐาน&nbsp;</span></span></span><span style="color:#808080"><span style="font-size:16px"><span style="font-family:arial,helvetica,sans-serif">(Median)</span></span></span><span style="color:#000000"><span style="font-size:16px"><span style="font-family:arial,helvetica,sans-serif"> หรือเรียกง่าย ๆ ว่าค่ากลาง <strong>ก็คือค่าที่อยู่ตรงกลาง</strong>หลังจากเรานำค่าทั้งหมดมาจับเรียงลำดับจากน้อยไปมาก เช่น<br />
<strong>ตัวอย่างที่ 1</strong>) มีข้อมูลตัวเลขอยู่ชุดหนึ่งได้แก่ 5, 10, 6, 9, 12<br />
&nbsp; <u>วิธีทำ</u> </span></span></span>
<div style="margin-left: 40px;"><span style="color:#000000"><span style="font-size:16px"><span style="font-family:arial,helvetica,sans-serif">1) ให้นำข้อมูลทั้งหมดมาเรียงลำดับจากน้อยไปหามาก</span></span></span></div>

<div style="margin-left: 80px;"><span style="color:#000000"><span style="font-size:16px"><span style="font-family:arial,helvetica,sans-serif">5, 6, 9, 10, 12</span></span></span></div>

<div style="margin-left: 40px;"><span style="color:#000000"><span style="font-size:16px"><span style="font-family:arial,helvetica,sans-serif">2) ตำแหน่งมัธยฐาน คือข้อมูลที่อยู่ตรงกลาง</span></span></span></div>

<div><span style="color:#000000"><span style="font-size:16px"><span style="font-family:arial,helvetica,sans-serif">&nbsp; <u>ตอบ</u>&nbsp;<strong>9</strong>&nbsp;<br />
<br />
<strong>ตัวอย่างที่ 2</strong>) มีข้อมูลตัวเลขอยู่ชุดหนึ่งได้แก่ 5, 10, 6, 9, 12, 0, 16, 20<br />
&nbsp;&nbsp;<u>วิธีทำ</u>&nbsp;</span></span></span>

<div style="margin-left: 40px;"><span style="color:#000000"><span style="font-size:16px"><span style="font-family:arial,helvetica,sans-serif">1) ให้นำข้อมูลทั้งหมดมาเรียงลำดับจากน้อยไปหามาก</span></span></span></div>

<div style="margin-left: 80px;"><span style="color:#000000"><span style="font-size:16px"><span style="font-family:arial,helvetica,sans-serif">0, 5, 6, 9, 10, 12, 16, 20</span></span></span></div>

<div style="margin-left: 40px;"><span style="color:#000000"><span style="font-size:16px"><span style="font-family:arial,helvetica,sans-serif">2) แต่จะเห็นว่ามันไม่มีค่าที่อยู่ตรงกลาง ถ้าเกิดกรณีนี้ขึ้นให้หาตำแหน่งกลางจุดที่ 1 โดย<u>นับจำนวนข้อมูลที่มีทั้งหมดแล้วหารด้วย 2</u></span></span></span></div>

<div style="margin-left: 80px;"><span style="color:#000000"><span style="font-size:16px"><span style="font-family:arial,helvetica,sans-serif">ตำแหน่งกลางจุดที่ 1 = 8 / 2&nbsp; = 4</span></span></span></div>

<div style="margin-left: 40px;"><span style="color:#000000"><span style="font-size:16px"><span style="font-family:arial,helvetica,sans-serif">3)&nbsp;</span></span><span style="font-family:arial,helvetica,sans-serif; font-size:16px">หาตำแหน่งกลางจุดที่ 2 โดย<u>นำตำแหน่งจุดที่ 1 มาบวก 1</u></span></span></div>

<div style="margin-left: 40px;"><span style="color:#000000"><span style="font-size:16px"><span style="font-family:arial,helvetica,sans-serif">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;</span></span><span style="font-family:arial,helvetica,sans-serif; font-size:16px">ตำแหน่งกลางจุดที่ 2 = 4+1 = 5<br />
4) นำค่าที่อยู่ในตำแหน่งกลางจุดที่ 1 และ 2 มาบวกกันแล้วหาร 2</span></span></div>

<div style="margin-left: 80px;"><span style="color:#000000"><span style="font-family:arial,helvetica,sans-serif; font-size:16px"><u>9 + 10</u>&nbsp; &nbsp;= 9.5<br />
&nbsp; &nbsp; 2</span></span></div>

<div><span style="color:#000000"><span style="font-size:16px"><span style="font-family:arial,helvetica,sans-serif">&nbsp;&nbsp;<u>ตอบ</u>&nbsp;<strong>9.5</strong></span></span></span></div>
<br />
<span style="color:#000000"><span style="font-size:16px"><span style="font-family:arial,helvetica,sans-serif">ช่วยเขียนโปรแกรมหาค่ามัธยฐานนี้ให้หน่อยครับ</span></span></span></div>

## 2. Input Specification

<span style="font-size:16px"><span style="font-family:arial,helvetica,sans-serif">1 บรรทัด เป็นชุดข้อมูลซึ่งเป็นจำนวนจริง แต่ละข้อมูลคั่นด้วย &quot;, &quot;</span></span>

## 3. Output Specification

<span style="font-size:16px"><span style="font-family:arial,helvetica,sans-serif">1 บรรทัด แสดงเป็นเลขทศนิยม 2 ตำแหน่ง</span></span>

## 4. ตัวอย่างจาก iJudge

### ตัวอย่างที่ 1
- **อินพุต**:
  ```text
  5, 10, 6, 9, 12
  ```
- **เอาต์พุต**:
  ```text
  9.00
  ```

### ตัวอย่างที่ 2
- **อินพุต**:
  ```text
  5, 10, 6, 9, 12, 0, 16, 20
  ```
- **เอาต์พุต**:
  ```text
  9.50
  ```

### ตัวอย่างที่ 3
- **อินพุต**:
  ```text
  7
  ```
- **เอาต์พุต**:
  ```text
  7.00
  ```

### ตัวอย่างที่ 4
- **อินพุต**:
  ```text
  3.5, 1.25, 8, 2
  ```
- **เอาต์พุต**:
  ```text
  2.75
  ```
