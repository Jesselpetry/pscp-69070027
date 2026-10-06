# OJ 3589: FibonacciRecursionV1

> - **iJudge cp_id**: 3589 — ภาษา Python
> - **เวลาจำกัด**: 1 วินาที | **หน่วยความจำ**: 32,768 KB

---

## 1. โจทย์จริงจาก iJudge

เลข Fibonacci ของ n จะมีค่าเท่ากับ ค่า Fibonacci ของ n-1 รวมกับ ค่า Fibonacci ของ n-2 เขียนเป็นสมการดังนี้<br />

F(n) = F(n-1) + F(n-2)<br />

โดยที่
F(0) = 0
F(1) = 1

เช่น
F(2) = F(1) + F(0) = 0 + 1 = 1
F(3) = F(2) + F(1) = 1 + 1 = 2

จงเขียนโปรแกรมหาค่า Fibonacci ของ n เช่น n = 10 จะมีค่า F(10) = 55<br />

<u><span style="color:rgb(255, 0, 0)"><strong>ห้ามใช้ [ ] for while range xrange bin oct hex *</strong></span></u>

## 2. Input Specification

จำนวนเต็ม 1 จำนวน คือ n

## 3. Output Specification

Fibonacci ลำดับที่ n หรือ F(n)

## 4. ตัวอย่างจาก iJudge

### ตัวอย่างที่ 1
- **อินพุต**:
  ```text
  10
  ```
- **เอาต์พุต**:
  ```text
  55
  ```

### ตัวอย่างที่ 2
- **อินพุต**:
  ```text
  1
  ```
- **เอาต์พุต**:
  ```text
  1
  ```

### ตัวอย่างที่ 3
- **อินพุต**:
  ```text
  20
  ```
- **เอาต์พุต**:
  ```text
  6765
  ```
