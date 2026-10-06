# OJ 3537: [LEARNING LOGS] Impostor

> - **iJudge cp_id**: 3537 — ภาษา Python
> - **เวลาจำกัด**: 1 วินาที | **หน่วยความจำ**: 32,000 KB

---

## 1. โจทย์จริงจาก iJudge

<img alt="" src="https://cdn-wp.thesportsrush.com/2020/10/68e15d56-screenshot-157.png" style="height:365px; width:650px" /><br />
<br />
มีกลุ่มคนอยู่กลุ่มหนึ่งอยู่ในยานอวกาศ ซึ่งมีผู้ที่แอบอ้างแฝงเข้ามาจำนวนหนึ่งจากเพื่อนร่วมทีมทั้งหมด<br />
สมาชิกทุกคนจึงโหวตกันเพื่อขับไล่ผู้หลอกลวงออกจากยานอวกาศให้ได้<br />
จงหาผู้ที่ยังอยู่ในยานอวกาศ และ ถูกขับไล่ออกนอกยานอวกาศไปแล้ว เป็นชื่อตามด้วยบทบาท<br />
(เรียงชื่อตามตัวอักษร)<br />
<br />
<u><span style="font-size:14px"><span style="color:rgb(255, 0, 0)">**พยายามใช้ Dict และ Dict Methods นะครับ</span></span></u>

## 2. Input Specification

หลายบรรทัด<br />
-เป็นใส่ชื่อและบทบาทระหว่างCrewmate หรือ Impostor จนกว่าจะเจอคำว่า Start<br />
-จากนั้นให้ใส่ผู้ที่ถูกโหวตไล่ออกไป จนกว่าจะเจอคำว่า End

## 3. Output Specification

หลายบรรทัด<br />
-บรรทัดแรกคือ จำนวน Impostor ที่เหลืออยู่ ตามด้วย Impostor Remains<br />
-บรรทัดต่อมาคือ ***Alive***<br />
-บรรทัดต่อมาเป็นชื่อผู้รอดชีวิตทุกคนตามด้วยบทบาทระหว่างCrewmate หรือ Impostor จนครบ<br />
-บรรทัดต่อมาคือ ***Dead***<br />
-บรรทัดที่เหลือคือชื่อผู้ที่เสียชีวิตตามด้วยบทบาทระหว่างCrewmate หรือ Impostor<br />
(เรียงตามตัวอักษร)

## 4. ตัวอย่างจาก iJudge

### ตัวอย่างที่ 1
- **อินพุต**:
  ```text
  {"Green" : "Crewmate"}
  {"Cyan" : "Crewmate"}
  {"Red" : "Crewmate"}
  {"Pink" : "Crewmate"}
  {"Lime" : "Impostor"}
  {"Blue" : "Impostor"}
  {"White" : "Crewmate"}
  {"Orange" : "Crewmate"}
  Start
  Green
  Cyan
  White
  End
  ```
- **เอาต์พุต**:
  ```text
  2 Impostor Remains
  ***Alive***
  Blue : Impostor
  Lime : Impostor
  Orange : Crewmate
  Pink : Crewmate
  Red : Crewmate
  ***Dead***
  Cyan : Crewmate
  Green : Crewmate
  White : Crewmate
  ```

### ตัวอย่างที่ 2
- **อินพุต**:
  ```text
  {"Aqua" : "Crewmate"}
  {"Suisei" : "Impostor"}
  {"Fubuki" : "Crewmate"}
  {"Matsuri" : "Impostor"}
  {"Impostor" : "Crewmate"}
  {"Pekora" : "Impostor"}
  {"Korone" : "Crewmate"}
  {"Rushia" : "Crewmate"}
  {"Kusa" : "Crewmate"}
  {"Yagoo" : "Crewmate"}
  {"Marine" : "Crewmate"}
  {"Pinkguy" : "Crewmate"}
  {"Crewmate" : "Impostor"}
  {"Watame" : "Crewmate"}
  Start
  Aqua
  Suisei
  Fubuki
  Matsuri
  Crewmate
  Pekora
  End
  ```
- **เอาต์พุต**:
  ```text
  0 Impostor Remains
  ***Alive***
  Impostor : Crewmate
  Korone : Crewmate
  Kusa : Crewmate
  Marine : Crewmate
  Pinkguy : Crewmate
  Rushia : Crewmate
  Watame : Crewmate
  Yagoo : Crewmate
  ***Dead***
  Aqua : Crewmate
  Crewmate : Impostor
  Fubuki : Crewmate
  Matsuri : Impostor
  Pekora : Impostor
  Suisei : Impostor
  ```
