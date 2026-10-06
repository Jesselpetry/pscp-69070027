# OJ 3539: iPhone 13 Again

> - **iJudge cp_id**: 3539 — ภาษา Python
> - **เวลาจำกัด**: 1 วินาที | **หน่วยความจำ**: 32,000 KB

---

## 1. โจทย์จริงจาก iJudge

<img alt="" src="https://ejudge.it.kmitl.ac.th/uploads/1632623456_iphone-13-pro-price-update-2021.jpeg" style="height:389px; width:879px" /><br />

จากการเช็คราคา iPhone 13 ซึ่งมี 4 รุ่น ที่&nbsp;https://www.apple.com/th/iphone/ เมื่อวันที่ 25 กันยายน 2564 พบว่าแต่ละรุ่นมี<span style="font-family:helvetica neue,helvetica,arial,tahoma,sans-serif; font-size:14px">ราคาเริ่มต้นเป็นดังนี้</span><br />
<span style="font-family:helvetica neue,helvetica,arial,tahoma,sans-serif; font-size:14px">iPhone 13 mini ราคาเริ่มต้น 25900 บาท</span><br />
<span style="font-family:helvetica neue,helvetica,arial,tahoma,sans-serif; font-size:14px">iPhone 13 ราคาเริ่มต้น 29900 บาท</span><br />
<span style="font-family:helvetica neue,helvetica,arial,tahoma,sans-serif; font-size:14px">iPhone 13 Pro ราคาเริ่มต้น 38900 บาท</span><br />
<span style="font-family:helvetica neue,helvetica,arial,tahoma,sans-serif; font-size:14px">iPhone 13 Pro Max ราคาเริ่มต้น 42900 บาท<br />

ทุกรุ่นที่ราคาเริ่มต้นจะมีความจุ 128 GB เท่ากัน แต่สามารถเลือกความจุเพิ่มได้<br />

จงหาราคาที่ผู้ซื้อต้องจ่ายหากซื้อรุ่น iPhone 13 และความจุ ที่ต้องการ หากไม่สามารถซื้อรุ่นที่ต้องการ หรือความจุที่ต้องการได้ ให้ตอบว่า Not Available<br />

**** รายละเอียดความจุของแต่ละรุ่น และราคาของความจุในแต่ละรุ่นให้ลองหาดูใน&nbsp;</span><s>https://www.apple.com/th/iphone/</s> เอาเอง<br />

**** เพื่อให้โจทย์ง่ายไม่ซับซ้อนเกินไป ราคาในข้อนี้ยังไม่รวมซื้อ AppleCare+<br />

***** เนื่องด้วย Iphone 13 pro และ Iphone 13 pro max ได้ถูกนำหน้าแสดงสินค้าออกไป จึงให้อ้างอิงราคาดังนี้
<br />
<p><strong>iPhone 13 mini</strong></p>

<ul>
	<li>128GB ราคา ฿25,900</li>
	<li>256GB ราคา ฿29,900</li>
	<li>512GB ราคา ฿37,900</li>
</ul>

<p><strong>iPhone 13</strong></p>

<ul>
	<li>128GB ราคา ฿29,900</li>
	<li>256GB ราคา ฿33,900</li>
	<li>512GB ราคา ฿41,900</li>
</ul>

<p><strong>iPhone 13 Pro</strong></p>

<ul>
	<li>128GB ราคา ฿38,900</li>
	<li>256GB ราคา ฿42,900</li>
	<li>512GB ราคา ฿50,900</li>
	<li>1TB ราคา&nbsp;฿58,900</li>
</ul>

<p><strong>iPhone 13 Pro Max</strong></p>

<ul>
	<li>128GB ราคา ฿42,900</li>
	<li>256GB ราคา ฿46,900</li>
	<li>512GB ราคา ฿54,900</li>
	<li>1TB ราคา ฿62,900</li>
</ul>
<span style="font-family:helvetica neue,helvetica,arial,tahoma,sans-serif; font-size:14px">&nbsp;</span><br />
&nbsp;

## 2. Input Specification

<u>**2 บรรทัด</u>**

**บรรทัดแรก :** เป็น String เป็นชื่อ รุ่นของโทรศัพท์ที่ต้องการจะซื้อ
**บรรทัดสอง :** เป็นความจุ เป็นตัวเลขจำนวนเต็ม เว้นวรรค และตามด้วยหน่วย (GB หรือ TB)

## 3. Output Specification

**บรรทัดเดียว :** เป็นราคาที่ต้องจ่าย เป็นจำนวนเต็มบวก 
หากไม่สามารถซื้อได้ ให้ตอบว่า `Not Available`

## 4. ตัวอย่างจาก iJudge

### ตัวอย่างที่ 1
- **อินพุต**:
  ```text
  iPhone 13 mini
  128 GB
  ```
- **เอาต์พุต**:
  ```text
  25900
  ```

### ตัวอย่างที่ 2
- **อินพุต**:
  ```text
  iPhone 13 Pro Max
  256 GB
  ```
- **เอาต์พุต**:
  ```text
  46900
  ```

### ตัวอย่างที่ 3
- **อินพุต**:
  ```text
  iPhone 13 Pro
  64 GB
  ```
- **เอาต์พุต**:
  ```text
  Not Available
  ```

### ตัวอย่างที่ 4
- **อินพุต**:
  ```text
  iPhone 14 Pro Super
  128 GB
  ```
- **เอาต์พุต**:
  ```text
  Not Available
  ```

### ตัวอย่างที่ 5
- **อินพุต**:
  ```text
  iPhone 13 mini
  1 TB
  ```
- **เอาต์พุต**:
  ```text
  Not Available
  ```
