# OJ 3529: CaesarV2

> - **iJudge cp_id**: 3529 — ภาษา Python
> - **เวลาจำกัด**: 1 วินาที | **หน่วยความจำ**: 32,000 KB

---

## 1. โจทย์จริงจาก iJudge

Caesar Cipher เป็นวิธีการเข้ารหัสง่ายๆแบบหนึ่ง<br />
วิธีการเข้ารหัสจะเป็นการแทนค่าตัวอักษร a-z และ A-Z ด้วยโดยการเลื่อน (Shift) ตัวอักษรตามจำนวนที่ผู้ส่งและผู้รับได้ตกลงกันไว้ล่วงหน้า<br />
ยกตัวอย่างเช่นเมื่อต้องการเข้ารหัสข้อความว่า The quick brown fox jumps over the lazy dog. ด้วยการเลื่อนตัวอักษรไปทางขวา (right shift) 3 ตัวอักษร<br />
ข้อความที่ถูกเข้ารหัสแล้วจะกลายเป็น Wkh txlfn eurzq ira mxpsv ryhu wkh odcb grj.<br />
<br />
จงเขียนโปรแกรมถอดรหัสข้อความที่ถูกเข้ารหัสด้วยวิธีการ Caesar Cipher <span style="color:#FF0000"><strong>โดยที่ไม่ทราบจำนวนครั้งของการเลื่อนตัวอักษร</strong></span>


ปล. ตัวอย่างคำที่สามารถพบได้ทั่วไปในบทความภาษาอังกฤษ:

"what", "when", "why", "which", "this", "there", "where", "the", "is", "am", "are", "you", "we", "they", "he", "she", "it"

## 2. Input Specification

ข้อความที่ถูกเข้ารหัสเป็นข้อความในบทความภาษาอังกฤษทั่วไป<br />
ตัวอักขระอื่นๆที่ไม่ใช่ตัวอักษร a-z และ A-Z เช่นตัวเลขหรืออักขระพิเศษจะไม่ได้ถูกเข้ารหัส<br />
&nbsp;

## 3. Output Specification

ข้อความที่ถอดรหัสแล้ว

## 4. ตัวอย่างจาก iJudge

### ตัวอย่างที่ 1
- **อินพุต**:
  ```text
  Wkh txlfn eurzq ira mxpsv ryhu wkh odcb grj.
  ```
- **เอาต์พุต**:
  ```text
  The quick brown fox jumps over the lazy dog.
  ```
