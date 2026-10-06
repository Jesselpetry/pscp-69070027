# OJ 3504: [MINI EXAM] Hamming

> - **iJudge cp_id**: 3504 — ภาษา Python
> - **เวลาจำกัด**: 1 วินาที | **หน่วยความจำ**: 32,000 KB

---

## 1. โจทย์จริงจาก iJudge

![](https://ijudge.it.kmitl.ac.th:7159/api/file/file/1728719861732_083875.png)
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;![](https://ijudge.it.kmitl.ac.th:7159/api/file/file/1728719870544_b9f800.png)

ในทาง<a href="https://th.wikipedia.org/wiki/%E0%B8%97%E0%B8%A4%E0%B8%A9%E0%B8%8E%E0%B8%B5%E0%B8%82%E0%B9%89%E0%B8%AD%E0%B8%A1%E0%B8%B9%E0%B8%A5" title="ทฤษฎีข้อมูล">ทฤษฎีข้อมูล</a>แล้ว&nbsp;<strong>ระยะทางแฮมมิง&nbsp;</strong>(<a href="https://th.wikipedia.org/wiki/%E0%B8%A0%E0%B8%B2%E0%B8%A9%E0%B8%B2%E0%B8%AD%E0%B8%B1%E0%B8%87%E0%B8%81%E0%B8%A4%E0%B8%A9" title="ภาษาอังกฤษ">อังกฤษ</a>:&nbsp;Hamming distance) ระหว่าง 2 ข้อความที่มีความยาวเท่ากัน คือจำนวนตำแหน่งที่มีสัญลักษณ์หรืออักขระที่แตกต่างกัน กล่าวอีกนัยหนึ่ง มันคือจำนวนน้อยที่สุดที่ต้องใช้เพื่อเปลี่ยนจากข้อความหนึ่งไปเป็นอีกข้อความหนึ่ง หรือจำนวนตัวอักษรที่<em>คลาดเคลื่อน</em>ที่เปลี่ยนจากข้อความหนึ่งไปเป็นอีกข้อความหนึ่ง
<h2>ตัวอย่าง[<a href="https://th.wikipedia.org/w/index.php?title=%E0%B8%A3%E0%B8%B0%E0%B8%A2%E0%B8%B0%E0%B8%97%E0%B8%B2%E0%B8%87%E0%B9%81%E0%B8%AE%E0%B8%A1%E0%B8%A1%E0%B8%B4%E0%B8%87&amp;action=edit&amp;section=1" title="แก้ไขส่วน: ตัวอย่าง">แก้</a>]</h2>

<p>ระยะทางแฮมมิงระหว่าง:</p>

![](https://ijudge.it.kmitl.ac.th:7159/api/file/file/1728720113281_60738a.png)

หมายเหตุ ลอกมาจาก wikipedia (ขี้เกียจพิมพ์เอง)

จงหา Hamming Distance ของข้อความ 2 ข้อความที่รับเข้ามา<p></p>

## 2. Input Specification

มี 2 บรรทัด แต่ละบรรทัดเป็นข้อความ string&nbsp; (ทั้ง 2 string มีขนาดความยาวเท่ากัน)

## 3. Output Specification

1 บรรทัด เป็นจำนวนเต็มบวกหรือศูนย์ เป็นระยะทาง Hamming (Hamming distance) ของ 2 ข้อความที่รับเข้ามา

## 4. ตัวอย่างจาก iJudge

### ตัวอย่างที่ 1
- **อินพุต**:
  ```text
  ความรัก
  ความสุข
  ```
- **เอาต์พุต**:
  ```text
  3
  ```

### ตัวอย่างที่ 2
- **อินพุต**:
  ```text
  1011101
  1001001
  ```
- **เอาต์พุต**:
  ```text
  2
  ```

### ตัวอย่างที่ 3
- **อินพุต**:
  ```text
  karolin
  kathrin
  ```
- **เอาต์พุต**:
  ```text
  3
  ```
