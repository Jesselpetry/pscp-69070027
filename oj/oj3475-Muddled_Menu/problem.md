# OJ 3475: Muddled Menu

> - **iJudge cp_id**: 3475 — ภาษา Python
> - **เวลาจำกัด**: 1 วินาที | **หน่วยความจำ**: 32,000 KB

---

## 1. โจทย์จริงจาก iJudge

มีร้านอาหารแห่งหนึ่งมีเมนู หลายคอส ก่อนเปิดร้านในแต่ละวันหัวหน้าเชฟจะไล่บอกพนักงานในร้านว่าเมนูวันนี้มีอะไรบ้าง<br />
แต่อาจไล่บอกไม่ตามลำดับ บางครั้งก็บอกผิดต้องเริ่มใหม่หมด หรือเกิดปัญหาต้องเอาคอสใดคอสหนึ่งออก<br />
พี่จึงอยากให้น้องๆเขียนโปรแกรมแสดงผลเมนูของร้านนี้ โดยจะแสดงทั้งตามลำดับคอสแรกจนสุดท้าย และจากคอสสุดท้ายสู่คอสแรก<br />
<br />
HINT: เราสามารถเก็บเป็น List และนำ List Method ต่างๆมาช่วยได้

## 2. Input Specification

หลายบรรทัด รับไปเรื่อยๆจนกว่าจะเจอคำว่า &quot;DONE&quot;<br />
-แต่ละบรรทัดประกอบด้วยชื่ออาหาร และหมายเลขคอส คั่นด้วย &quot; #&quot; หากหมายเลขคอสเป็น #N ให้ต่อท้ายสุดของเมนูในขณะนั้น หากเป็น #จำนวนเต็มบวก ให้แทรกไปในตำแหน่งนั้น (เริ่มนับจาก 1)<br />
-หากเมนูมีปัญหาแล้วต้องเริ่มนับใหม่จะ input &quot;SOMETHING&#39;S WRONG&quot; ให้ลบเมนูที่เก็บไว้ แล้วเริ่มรับชื่ออาหารใหม่<br />
-หากไม่สามารถทำอาหารเมนูใหนได้ จะ input ว่า &quot;Can&#39;t do: &quot; ตามด้วยชื่ออาหารที่ทำไม่ได้&nbsp;แล้วให้ลบออกจากคอส<br />
-หากเกิดภัยธรรมชาติร้านปิดกระทันหัน ให้ input ว่า CLOSED แล้วลบเมนูอาหารออกทั้งหมด จากนั้นจบการรับ input

## 3. Output Specification

บรรทัดเดียวคือ เมนูของร้านนี้ทั้งตามลำดับคอสแรกจนสุดท้าย และจากคอสสุดท้ายสู่คอสแรก (ตาม sample case)

## 4. ตัวอย่างจาก iJudge

### ตัวอย่างที่ 1
- **อินพุต**:
  ```text
  Abbacchio al forno #1
  Panna Cotta #N
  Beef Stew #2
  Can't do: Abbacchio al forno
  DONE
  ```
- **เอาต์พุต**:
  ```text
  Full Course: ['Beef Stew', 'Panna Cotta'] Reversed: ['Panna Cotta', 'Beef Stew']
  ```

### ตัวอย่างที่ 2
- **อินพุต**:
  ```text
  Boiled Eggs #N
  Steamed Eggs #2
  SOMETHING'S WRONG
  Borscht #1
  Buccellati #N
  Wagyu Steak #2
  Gelato #3
  Tapas #4
  Risotto #4
  DONE
  ```
- **เอาต์พุต**:
  ```text
  Full Course: ['Borscht', 'Wagyu Steak', 'Gelato', 'Risotto', 'Tapas', 'Buccellati'] Reversed: ['Buccellati', 'Tapas', 'Risotto', 'Gelato', 'Wagyu Steak', 'Borscht']
  ```

### ตัวอย่างที่ 3
- **อินพุต**:
  ```text
  Rice #1
  Boiled Eggs #N
  CLOSED
  ```
- **เอาต์พุต**:
  ```text
  Full Course: [] Reversed: []
  ```
