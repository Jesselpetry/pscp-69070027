# OJ 3477: [LEARNING LOGS] Pad Thai

> - **iJudge cp_id**: 3477 — ภาษา Python
> - **เวลาจำกัด**: 1 วินาที | **หน่วยความจำ**: 32,000 KB

---

## 1. โจทย์จริงจาก iJudge

<img alt="" src="https://www.thipkitchen.com/images/course/padthai/img1.jpg" style="height:511px; width:680px" /><br />
<br />
มาทำผัดไทยกินกันเถอะ!!!<br />
โดยคุณรับบทเป็นคนทำผัดไทยให้เชฟชื่อดังแห่งนึงในเมืองไทยลองชิม<br />
แต่มีเงื่อนไขว่าผัดไทยที่ทำนั้นต้องมีวัตถุดิบ/ส่วนผสมที่เชฟกำหนดให้เท่านั้นห้ามใส่วัตถุดิบหรือส่วนผสมนอกเหนือจากสูตรที่เชฟให้มาเด็ดขาด<br />
วัตถุดิบในการทำผัดไทย :<br />
1.&nbsp; Pad Thai Sauce<br />
2.&nbsp; Tofu<br />
3.&nbsp; Pickle Turnip<br />
4.&nbsp; Shrimp<br />
5.&nbsp; Bean Sprouts<br />
6.&nbsp; Noodle<br />
7.&nbsp; Chives<br />
8.&nbsp; Lime<br />
9.&nbsp; Egg<br />
10. Oil<br />
11. Peanuts<br />
<br />
ตามสูตรแล้วอาจจะมีวัตถุดิบมากกว่านี้เพื่อให้ผัดไทยอร่อยขึ้น แต่เชฟยังไม่ยอมรับ&nbsp;<br />
ดังนั้นจงใช้วัตถุดิบเหล่านี้ในการทำเท่านั้น<br />
<br />
เมื่อคุณทำเสร็จแล้วผัดไทยจะต้องมีรสชาติ 3 อย่างนี้ถึงจะอร่อยคือ<br />
1. Sweet<br />
2. Sour<br />
3. Salty<br />
<br />
หากคุณใช้วัตถุดิบในการทำผัดไทยไม่ครบ เชฟจะไม่สนใจรสชาติ เชฟจะบอกกับคุณว่า &quot;This is bad!&quot;<br />
หากคุณใช้วัตถุดิบในการทำผัดไทยครบตามที่กำหนดแต่รสชาติยังไม่ครบหรือมีรสอื่น เชฟจะบอกกับคุณว่า &quot;Not Bad...&quot;<br />
หากคุณใช้วัตถุดิบในการทำผัดไทยที่ไม่ได้อยู่ในส่วนผสมที่เขียนไว้ข้างต้น (วัตถุดิบที่เขียนไว้ข้างต้นจะครบหรือไม่ครบก็ตาม) เชฟจะไม่สนใจรสชาติ เชฟจะบอกกับคุณว่า &quot;This is not Pad Thai!!!&quot;<br />
หากคุณใช้วัตถุดิบในการทำผัดไทยครบและรสชาติครบทั้ง 3 อย่าง เชฟจะรู้สึกถูกปากจนต้องพูดออกมาว่า &quot;Delicious!&quot;<br />
<br />
คุณมีเวลาไม่มากในการทำ ดังนั้นตั้งใจทำให้สุดฝีมือ&nbsp;<br />
อื้ม~~ อาโหร่ยยยย~~~

## 2. Input Specification

หลายบรรทัด : ให้รับข้อความเข้ามาเรื่อยๆที่เป็นวัตถุดิบจนกว่าจะเจอคำว่า &quot;Cook&quot;<br />
หลายบรรทัด : ให้รับข้อความเข้ามาเรื่อยๆที่เป็นรสชาติของผัดไทยจนกว่าจะเจอคำว่า &quot;End&quot;

## 3. Output Specification

หนึ่งบรรทัด : คือประโยคที่เชฟพูดออกมา

## 4. ตัวอย่างจาก iJudge

### ตัวอย่างที่ 1
- **อินพุต**:
  ```text
  Pad Thai Sauce
  Tofu
  Pickle Turnip
  Shrimp
  Bean Sprouts
  Noodle
  Chives
  Lime
  Egg
  Peanuts
  Cook
  Sweet
  Sour
  End
  ```
- **เอาต์พุต**:
  ```text
  This is bad!
  ```

### ตัวอย่างที่ 2
- **อินพุต**:
  ```text
  Pad Thai Sauce
  Tofu
  Tofu
  Pickle Turnip
  Shrimp
  Bean Sprouts
  Noodle
  Chives
  Lime
  Egg
  Oil
  Egg
  Peanuts
  Cook
  Sweet
  Sour
  Salty
  Sweet
  End
  ```
- **เอาต์พุต**:
  ```text
  Delicious!
  ```

### ตัวอย่างที่ 3
- **อินพุต**:
  ```text
  Pad Thai Sauce
  Tofu
  Pickle Turnip
  Shrimp
  Bean Sprouts
  Noodle
  Chives
  Lime
  Egg
  Oil
  Peanuts
  Cook
  Sweet
  Sour
  Salty
  Bitter
  End
  ```
- **เอาต์พุต**:
  ```text
  Not Bad...
  ```
