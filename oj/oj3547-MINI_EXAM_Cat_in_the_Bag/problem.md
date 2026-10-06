# OJ 3547: [ MINI EXAM ] Cat in the Bag

> - **iJudge cp_id**: 3547 — ภาษา Python
> - **เวลาจำกัด**: 1 วินาที | **หน่วยความจำ**: 32,000 KB

---

## 1. โจทย์จริงจาก iJudge

![Cat in bag](https://transcode-v2.app.engoo.com/image/fetch/f_auto,c_lfill,w_300,dpr_3/https://assets.app.engoo.com/images/3MI6CnfHBSiZMixcjIv25D.jpeg)

# นี้คือแมวในกระเป๋า

สายการบิน PSCP-2025 ของเรานั้นมีมาตราการณ์ที่ว่าห้ามนำแมวขึ้นเครื่องบิน เนื่องจาก กัปตันผู้ขับเครื่องบินของเรานั้น **<u>แพ้ขนแมว</u>** ดังนั้นเราจึงต้องมีการตรวจกระเป๋ากันอย่างเข้มข้นโดยการขอตรวจกระเป๋าของผู้โดยสารทุกคน **หากผู้โดยสารท่านใดมีคำว่า cat อยู่จะต้องนำเข้า ลิสต์ต้องห้ามเพื่อไม่ให้ขึ้นในสายการบินรอบนี้** เพราะจะทำให้ กัปตันของเรานั้นไม่สามารถทำงานต่อได้ หน้าที่นี้จึงตกเป็นของลูกเรือหน้าใหม่ของเราในการตรวจกระเป๋าผู้โดยสาร

## 2. Input Specification

**<u>หลายบรรทัด รับเข้ามาเรื่อยๆ จนเจอ -1</u>**
เป็นรายชื่อกระเป๋าของผู้โดยสาร

## 3. Output Specification

**<u>2บรรทัด</u>**
`"The number of cat in bag {number}"`
`"List of cat {lst}"` **โดยรายชื่อกระเป๋าทุกใบจะเป็นตัวเล็กหมด**

## 4. ตัวอย่างจาก iJudge

### ตัวอย่างที่ 1
- **อินพุต**:
  ```text
  bag's Miss.cat
  bag's Karn Suddee
  bag's TaiKie
  bag's catkung
  bag's dogie
  -1
  ```
- **เอาต์พุต**:
  ```text
  The number of cat in bag 2
  List of cat ["bag's miss.cat", "bag's catkung"]
  ```

### ตัวอย่างที่ 2
- **อินพุต**:
  ```text
  bag's scottish cat
  bag's nat
  bag's meow cat
  bag's Mr.cat at Ayutthaya
  -1
  ```
- **เอาต์พุต**:
  ```text
  The number of cat in bag 3
  List of cat ["bag's scottish cat", "bag's meow cat", "bag's mr.cat at ayutthaya"]
  ```
