# OJ 3532: GCD_v2

> - **iJudge cp_id**: 3532 — ภาษา Python
> - **เวลาจำกัด**: 1 วินาที | **หน่วยความจำ**: 32,000 KB

---

## 1. โจทย์จริงจาก iJudge

<span style="font-family:source sans pro,sans-serif; font-size:14px">ในคณิตศาสตร์ ตัวหารร่วมมาก หรือ ห.ร.ม. ของจำนวนเต็มสองจำนวนซึ่งไม่เป็นศูนย์พร้อมกัน คือจำนวนเต็มที่มากที่สุดที่หารทั้งสองจำนวนลงตัว</span><br />

<strong>ตัวอย่าง</strong>
<span style="font-family:source sans pro,sans-serif; font-size:14px">ห.ร.ม. ของ 12 และ 18 = 6</span>
<span style="font-family:source sans pro,sans-serif; font-size:14px">ห.ร.ม. ของ 4 และ 14 = 2</span>
<span style="font-family:source sans pro,sans-serif; font-size:14px">ห.ร.ม. ของ 5 และ 0 = 5</span><br />

<span style="font-family:source sans pro,sans-serif; font-size:14px">จงเขียนโปรแกรมหา ห.ร.ม. ของจำนวน 2 จำนวน<br />

<span style="color:#FF0000">ลองเอาโปรแกรมที่เขียนและผ่าน GCD_v1 มาทดสอบก่อนว่าผ่านไหม ถ้าไม่ผ่าน ให้หา Algorithm ใหม่</span></span>

## 2. Input Specification

<span style="font-family:source sans pro,sans-serif; font-size:14px">2 บรรทัด เป็นจำนวนจริง จำนวนละ 1 บรรทัด</span><br />

<span style="font-family:source sans pro,sans-serif; font-size:14px">GCD v2 , Input มีค่าไม่น้อยกว่า 10 ล้าน</span>

## 3. Output Specification

<span style="font-family:source sans pro,sans-serif; font-size:14px">ห.ร.ม. ของจำนวน 2 จำนวนนั้น</span>

## 4. ตัวอย่างจาก iJudge

### ตัวอย่างที่ 1
- **อินพุต**:
  ```text
  22685530
  166489540
  ```
- **เอาต์พุต**:
  ```text
  48370
  ```

### ตัวอย่างที่ 2
- **อินพุต**:
  ```text
  181503190
  149626034
  ```
- **เอาต์พุต**:
  ```text
  70214
  ```

### ตัวอย่างที่ 3
- **อินพุต**:
  ```text
  290352808
  967466245
  ```
- **เอาต์พุต**:
  ```text
  1
  ```

### ตัวอย่างที่ 4
- **อินพุต**:
  ```text
  27182818
  0
  ```
- **เอาต์พุต**:
  ```text
  27182818
  ```
