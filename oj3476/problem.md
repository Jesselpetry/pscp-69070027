# OJ 3476: [LEARNING LOGS] CuteCat CuteFox

> - **iJudge cp_id**: 3476 — ภาษา Python
> - **เวลาจำกัด**: 1 วินาที | **หน่วยความจำ**: 32,000 KB

---

## 1. โจทย์จริงจาก iJudge

<img alt="" src="https://media1.tenor.com/images/abb2dd90f2d5b836e78ebc9c1f544a09/tenor.gif" style="height:401px; width:450px" /><br />
<br />
แมวน่ารักมากๆ ยิ่งเจอฝูงแมวอยู่ด้วยกันแล้วยิ่งน่ารักขึ้นไปอีก แต่ในฝูงแมวกลับมีแมวหน้าตาประหลาดปนมาด้วยซะงั้น<br />
จริงๆแล้วไม่ใช่แมวเอเลี่ยนแต่อย่างใดแต่มันคือจิ้งจอกผู้น่ารักต่างหาก<br />
แมวและจิ้งจอกแต่ละตัวจะมีหมายเลขติดเอาไว้ด้วย<br />
<span style="color:#FF0000">โดยปกติในฝูงแมวแสนจะน่ารักจะมีจิ้งจอกและแมวแสนน่ารักอย่างละ 1 ตัวซึ่งเป็นหมายเลขหนึ่งคือ แมว(Cat01)จะชื่อว่า Garfield จิ้งจอก(Fox01)จะชื่อว่า Fubuki&nbsp; (เช่น ไม่มีการกำหนด Cat01 หรือ Fox01 ก็จะให้เป็นตามข้างต้นนั้นเอง)</span><br />
แน่นอนว่าจะไม่มีชื่อที่ซ้ำกันหรือหมายเลขที่ซ้ำกัน<br />
ให้ตามหาแมวและจิ้งจอกว่ามีทั้งหมดกี่ตัว ชื่ออะไรบ้าง<br />
ให้แสดงชื่อก่อนแล้วตามด้วยชนิด(แมวหรือจิ้งจอก)และตัวเลข<br />
<br />
<u><span style="font-size:14px"><span style="color:#FF0000">**พยายามใช้ Dict และ Dict Methods นะครับ</span></span></u>

## 2. Input Specification

n+1 บรรทัด&nbsp;<br />
บรรทัดแรก เป็นจำนวนแมวและจิ้งจอกทั้งหมดหรือเกือบทั้งหมดในฝูง<br />
บรรดทัดที่ 2 ถึง n+1 เป็น dict ที่ประกอบไปด้วย key เเละ value ที่เป็นข้อมูลของฝูงแมวแสนน่ารัก<br />
(key เเละ value เป็น string อย่างแน่นอน)

## 3. Output Specification

หลายบรรทัด<br />
บรรทัดแรกคือจำนวนแมวทั้งหมด<br />
บรรทัดที่สองคือจำนวนจิ้งจอกทั้งหมด<br />
บรรทัดที่เหลือคือชื่อแมวทั้งหมดตามด้วยหมายเลข จากนั้นเป็นชื่อของจิ้งจอกตามด้วยหมายเลข<br />
(เรียงตามหมายเลข)

## 4. ตัวอย่างจาก iJudge

### ตัวอย่างที่ 1
- **อินพุต**:
  ```text
  5
  {"Chi" : "Cat06"}
  {"Tom" : "Cat05"}
  {"Shiro" : "Fox02"}
  {"Senko" : "Fox10"}
  {"Chocola" : "Cat03"}
  ```
- **เอาต์พุต**:
  ```text
  Cat : 4
  Fox : 3
  Garfield : Cat01
  Chocola : Cat03
  Tom : Cat05
  Chi : Cat06
  Fubuki : Fox01
  Shiro : Fox02
  Senko : Fox10
  ```

### ตัวอย่างที่ 2
- **อินพุต**:
  ```text
  4
  {"Vanilla" : "Cat01"}
  {"Okayu" : "Cat03"}
  {"Kuro" : "Fox02"}
  {"Pepper" : "Cat07"}
  ```
- **เอาต์พุต**:
  ```text
  Cat : 3
  Fox : 2
  Vanilla : Cat01
  Okayu : Cat03
  Pepper : Cat07
  Fubuki : Fox01
  Kuro : Fox02
  ```

### ตัวอย่างที่ 3
- **อินพุต**:
  ```text
  7
  {"Fubuki" : "Fox05"}
  {"Shiro" : "Fox01"}
  {"Garfield" : "Fox06"}
  {"Kin" : "Cat05"}
  {"Okayu" : "Cat03"}
  {"Kuro" : "Fox02"}
  {"Tom" : "Cat07"}
  ```
- **เอาต์พุต**:
  ```text
  Cat : 3
  Fox : 4
  Okayu : Cat03
  Kin : Cat05
  Tom : Cat07
  Shiro : Fox01
  Kuro : Fox02
  Fubuki : Fox05
  Garfield : Fox06
  ```
