# OJ 3293: [LEARNING LOGS] BigFrame

> - **iJudge cp_id**: 3293 — ภาษา Python
> - **เวลาจำกัด**: 1 วินาที | **หน่วยความจำ**: 32,000 KB

---

## 1. โจทย์จริงจาก iJudge

<img alt="" src="https://ejudge.it.kmitl.ac.th/uploads/1504954122_fiskbo-frame-blue__0315689_pe513656_s4.jpg" style="height:500px; width:500px" />
รับค่า string เข้ามา 5 บรรทัด และแสดงค่าตัวอักษรที่อยู่ใน string นั้นในกรอบรูปสี่เหลี่ยม ดังตัวอย่างใน test case ด้านล่าง

## 2. Input Specification

ข้อความขนาดตั้งแต่ 0 ตัวอักษร (ที่เป็น a-z, A-Z, 0-9 และเว้นวรรค)&nbsp; เป็นต้นไป จำนวน 5 บรรทัด
<br />
แนะนำว่าให้ทดสอบ Sample test cases โดยการ copy Input

## 3. Output Specification

ข้อความจำนวน 7 บรรทัดโดยจะมี space ระหว่างข้อความและกรอบซ้ายและขวาด้านละ&nbsp; 1 ช่อง ตามตัวอย่าง
<br />
กรอบซ้ายและกรอบขวาต้องห่างกันอย่างน้อย 2 space<br />
&nbsp;

## 4. ตัวอย่างจาก iJudge

### ตัวอย่างที่ 1
- **อินพุต**:
  ```text
  Hello World       
  in 
  a 
  big
  frame
  ```
- **เอาต์พุต**:
  ```text
  ***************
  * Hello World *
  * in          *
  * a           *
  * big         *
  * frame       *
  ***************
  ```

### ตัวอย่างที่ 2
- **อินพุต**:
  ```text
  Hello
  World in      
  a
  
  big frame
  ```
- **เอาต์พุต**:
  ```text
  *************
  * Hello     *
  * World in  *
  * a         *
  *           *
  * big frame *
  *************
  ```
