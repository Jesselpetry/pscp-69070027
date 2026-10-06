# OJ 3593: FibonacciRecursionV2

> - **iJudge cp_id**: 3593 — ภาษา Python
> - **เวลาจำกัด**: 1 วินาที | **หน่วยความจำ**: 32,768 KB

---

## 1. โจทย์จริงจาก iJudge

<span style="font-family:helvetica neue,helvetica,arial,tahoma,sans-serif; font-size:14px">ลำดับ Fibonacci เป็นลำดับเลขชนิดพิเศษที่ไม่เหมือนกับลำดับเลขคณิต หรือเรขาคณิตทั่วไป</span><br />
<br />
<span style="font-family:helvetica neue,helvetica,arial,tahoma,sans-serif; font-size:14px">โดยที่ลำดับ Fibonacci จะมีการนิยามสองลำดับแรกดังนี้</span><br />
<span style="font-family:helvetica neue,helvetica,arial,tahoma,sans-serif; font-size:14px">F(0) = 0 ; ลำดับที่ 0</span><br />
<span style="font-family:helvetica neue,helvetica,arial,tahoma,sans-serif; font-size:14px">F(1) = 1 ; ลำดับที่ 1</span><br />
<span style="font-family:helvetica neue,helvetica,arial,tahoma,sans-serif; font-size:14px">นอกเหนือจากลำดับดังกล่าว จะถูกสร้างขึ้นมาจากผลรวมของลำดับสองตัวก่อนหน้า</span><br />
<span style="font-family:helvetica neue,helvetica,arial,tahoma,sans-serif; font-size:14px">F(N) = F(N-1) + F(N-2)</span><br />
<br />
<span style="font-family:helvetica neue,helvetica,arial,tahoma,sans-serif; font-size:14px">ลำดับ Fibonacci จะมีการเรียงที่ตายตัวดังนี้</span><br />
<span style="font-family:helvetica neue,helvetica,arial,tahoma,sans-serif; font-size:14px">0, 1, 1, 2, 3, 5, 8, 13, ...</span><br />
<br />
<span style="font-family:helvetica neue,helvetica,arial,tahoma,sans-serif; font-size:14px">งานของคุณคือ ให้หาลำดับ Fibonacci ลำดับที่ N<br />

<br />
<strong>ให้ใช้ Recursion แต่มีข้อควรระวังคือมีให้หาลำดับที่ เกิน 1000 </strong></span><br />
<br />
​
---------------------------------------------------------------

10/25 ของ Testcases จะทำงานภายใน 1 วินาทีหากใช้ Recursion stack ธรรมดา<br />
20/25 ของ Testcases จะทำงานภายใน 1 วินาทีหากใช้ Recursion + Memorization</span><br />
21/25 ของ Testcases จะทำงานภายใน 1 วินาทีหากใช้ Recursion + Memorization + Recursive&nbsp;Optimization อีกนิดหน่อย<br />
25/25&nbsp;ของ Testcases จะทำงานภายใน 1 วินาทีหากทำการปรับปรุงการใช้งาน Recursion เพิ่มเติม

## 2. Input Specification

<span style="font-family:helvetica neue,helvetica,arial,tahoma,sans-serif; font-size:14px">หนึ่งบรรทัด N</span>

## 3. Output Specification

<span style="font-family:helvetica neue,helvetica,arial,tahoma,sans-serif; font-size:14px">หนึ่งบรรทัด เป็นลำดับ Fibonacci ลำดับที่ N<br />
<br />

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
  14
  ```
- **เอาต์พุต**:
  ```text
  377
  ```
