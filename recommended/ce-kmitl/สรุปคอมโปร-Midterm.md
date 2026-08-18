# สรุปเนื้อหา 01006012 Computer Programming
### (KMITL — ภาควิชาวิศวกรรมคอมพิวเตอร์) สำหรับสอบกลางภาค

**ครอบคลุม:** บทที่ 1–5 จากสไลด์ทั้งหมด + เนื้อหาจาก Cheat sheet
(บทที่ 1 พื้นฐานคอมพิวเตอร์ • บทที่ 2 ตัวแปร/นิพจน์/รับ-แสดงผล • บทที่ 3 เงื่อนไข • บทที่ 4 while • บทที่ 5 for • ภาคผนวก: list/string method/function/dict/tuple/file)

---

# บทที่ 1 ความรู้พื้นฐานเกี่ยวกับคอมพิวเตอร์

## 1.1 คอมพิวเตอร์คืออะไร
อุปกรณ์อิเล็กทรอนิกส์ที่มนุษย์ประดิษฐ์ขึ้น เพื่อเสริมความสามารถของมนุษย์ในด้าน **การรับรู้ การจำ การคำนวณ การเปรียบเทียบตัดสินใจ**

## 1.2 องค์ประกอบหลักของระบบคอมพิวเตอร์

| องค์ประกอบ | ความหมาย |
|---|---|
| **ฮาร์ดแวร์ (Hardware)** | ส่วนประกอบทางอิเล็กทรอนิกส์และแมคคานิกส์ทั้งหมดที่ **จับต้องได้** |
| **ซอฟต์แวร์ (Software)** | ส่วนที่เป็นชุดคำสั่งหรือโปรแกรมที่สั่งงานภายในระบบ |

### ส่วนประกอบหลักของฮาร์ดแวร์ (4 ส่วน)

1. **หน่วยประมวลผลกลาง (CPU)** — คำนวณทางคณิตศาสตร์และประมวลผลทางตรรกศาสตร์ บางครั้งเรียกว่า *ไมโครโปรเซสเซอร์* เช่น Intel Core i7, AMD Ryzen 7
2. **หน่วยเก็บข้อมูล** — แบ่ง 2 ส่วนย่อย
   - เก็บชั่วคราว ต้องใช้กระแสไฟฟ้าหล่อเลี้ยง (volatile) เช่น **SDRAM**
   - เก็บถาวร (non-volatile) เช่น **ฮาร์ดดิสก์ ซีดีรอม**
3. **หน่วยนำเข้าข้อมูล (Input)** — คีย์บอร์ด เมาส์ กล้อง touchscreen
4. **หน่วยส่งออกข้อมูล (Output)** — จอภาพ เครื่องพิมพ์ เครื่องฉายภาพ ลำโพง

## 1.3 ซอฟต์แวร์

**ซอฟต์แวร์** = ชุดคำสั่งที่ควบคุมการทำงานของคอมพิวเตอร์ (เรียกอีกอย่างว่า *โปรแกรมคอมพิวเตอร์*)

**ซอฟต์แวร์ระบบ (System Software)** = ซอฟต์แวร์หลักที่ถูกเรียกใช้ในระบบ ควบคุมฮาร์ดแวร์ และเป็นตัวกลางติดต่อกับผู้ใช้

### ระบบปฏิบัติการที่ต้องจำ

| OS | ปี | จุดเด่น | ภาษาที่ใช้สร้าง |
|---|---|---|---|
| **DOS** (Disk Operating System) | 1981–1995 | สั่งงานผ่าน **command line** เช่น `dir` เพื่อดูจำนวนไฟล์ | – |
| **Windows** | 1985–ปัจจุบัน | ระบบ **GUI** (Graphic User Interface) | C/C++ และ Assembly |
| **OS/2** | 1987–2001 | พัฒนาโดย Microsoft + IBM ช่วงแรก ต่อมา IBM พัฒนาต่อ | C/C++ |
| **Unix** | 1970–ปัจจุบัน | พัฒนาที่ **Bell Lab., AT&T** | – |

## 1.4 ภาษาคอมพิวเตอร์ (3 ระดับ)

1. **ภาษาเครื่อง (Machine Language)** — ประกอบด้วยเลข 0 กับ 1 สั่งให้คอมพิวเตอร์ทำงานได้ทันที ข้อเสียคือเขียนยาก
2. **ภาษา Assembly** — กึ่งภาษาเครื่อง เขียนเป็นคำสั่ง **Mnemonic** แปลงเป็นภาษาเครื่องได้ง่ายโดยเทียบตาราง หรือใช้ **Assembler**
3. **ภาษาขั้นสูง (High-level)** — ใกล้เคียงภาษามนุษย์ เช่น C, PASCAL, FORTRAN, **Python** เขียนง่าย แต่ต้องแปลเป็นภาษาเครื่องก่อน

### วิธีแปลภาษาขั้นสูงเป็นภาษาเครื่อง ⭐ ออกสอบบ่อย

| ตัวแปลภาษา | วิธีทำงาน | ตัวอย่างภาษา |
|---|---|---|
| **Interpreter** (อินเตอร์พรีเตอร์) | แปล **ทีละคำสั่ง** แล้วส่งให้เครื่องทำงาน จากนั้นจึงแปลคำสั่งถัดไป | **Python**, Java, Perl, shell script, VB script |
| **Compiler** (คอมไพเลอร์) | แปล **ทั้งหมด** ก่อน แล้วจึงส่งให้เครื่องทำงาน | C, C++, Pascal |

> Python เป็นภาษาแบบ **Interpreter**

## 1.5 ระบบตัวเลข

- **ฐานสิบ (Decimal)** ใช้เลข 0–9 : (527)₁₀ = 5×10² + 2×10¹ + 7×10⁰
- **ฐานสอง (Binary)** ใช้เลข 0, 1 : (101)₂ = 1×2² + 0×2¹ + 1×2⁰ = 5
- **ฐานสิบหก (Hexadecimal)** ใช้ 0–9 และ A–F : (3B2)₁₆ = 3×16² + 11×16¹ + 2×16⁰ = 946

> **ระบบตัวเลขที่ใช้ในคอมพิวเตอร์คือ ระบบเลขฐานสอง**

### การแปลงฐานสอง → ฐานสิบ
คูณน้ำหนักแต่ละบิต (2⁰, 2¹, 2², …) แล้วบวกกัน

ตัวอย่าง `10110101₂`

| บิต | 1 | 0 | 1 | 1 | 0 | 1 | 0 | 1 |
|---|---|---|---|---|---|---|---|---|
| น้ำหนัก | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |

= 128 + 0 + 32 + 16 + 0 + 4 + 0 + 1 = **181**

### การแปลงฐานสิบ → ฐานสอง
หารด้วย 2 ไปเรื่อย ๆ เก็บเศษ อ่านเศษจากล่างขึ้นบน

```
2 ) 43
2 ) 21  เศษ 1   ← LSB (Least Significant Bit)
2 ) 10  เศษ 1
2 )  5  เศษ 0
2 )  2  เศษ 1
2 )  1  เศษ 0
       เศษ 1   ← MSB (Most Significant Bit)
43₁₀ = 101011₂
```

### การแปลงฐานสิบ → ฐานสิบหก
หารด้วย 16 เก็บเศษ (เศษ 10–15 เขียนเป็น A–F)

```
16 ) 946
16 )  59  เศษ 2
16 )   3  เศษ 11 = B
        เศษ 3
946₁₀ = 3B2₁₆
```

### ตารางแปลงฐานสิบหก ↔ ฐานสอง (ต้องจำ) ⭐

| Hex | Binary | Hex | Binary |
|---|---|---|---|
| 0 | 0000 | 8 | 1000 |
| 1 | 0001 | 9 | 1001 |
| 2 | 0010 | A | 1010 |
| 3 | 0011 | B | 1011 |
| 4 | 0100 | C | 1100 |
| 5 | 0101 | D | 1101 |
| 6 | 0110 | E | 1110 |
| 7 | 0111 | F | 1111 |

> **เทคนิค:** ฐาน 16 หนึ่งหลัก = ฐาน 2 สี่บิตเสมอ (จับกลุ่มทีละ 4 บิตจากขวามาซ้าย)

## 1.6 ขนาดตัวเลขของเครื่องคอมพิวเตอร์ ⭐

| หน่วย | ขนาด |
|---|---|
| **บิต (bit)** | เลขฐานสองเพียงตัวเดียว (bit = **bi**nary dig**it**) |
| **ไบต์ (Byte)** | 8 บิต |
| **เวิร์ด (Word)** | 16 บิต = 2 ไบต์ |
| **กิโลไบต์ (KB)** | 2¹⁰ = 1,024 ไบต์ |
| **เมกะไบต์ (MB)** | 2¹⁰ × 2¹⁰ ไบต์ |
| **จิกะไบต์ (GB)** | 2¹⁰ × 2¹⁰ × 2¹⁰ ไบต์ |

## 1.7 ตัวอักษรที่ใช้ในคอมพิวเตอร์ — รหัส ASCII ⭐

- ข้อมูลที่เป็นตัวอักษรและสัญลักษณ์ ใช้ **รหัสแอสกี (ASCII)** ขนาด **8 บิต**
- กำหนดโดย **ANSI** (American National Standard Institute)
- ASCII = American National Standard Code for Information Interchange

| ตัวอักษร | ฐานสิบ | ฐานสิบหก |
|---|---|---|
| `A` | 65 | 41 |
| `B` | 66 | 42 |
| `a` | 97 | 61 |
| `'0'` | 48 | 30 |
| `'7'` | 55 | 37 |

> วิธีอ่านตาราง ASCII: **แถว = หลักสิบหกตัวหน้า, คอลัมน์ = หลักสิบหกตัวหลัง**

### ข้อสังเกตในการเก็บค่าลงหน่วยความจำ ⭐⭐

ตัวเลข **7** (เป็นค่าตัวเลข):
- เก็บแบบ 1 byte → `00000111` (= 4+2+1 = 7)
- เก็บแบบ integer (2 byte) → `00000000 00000111`

ตัวอักษร **'7'** (เป็นอักขระ):
- เก็บเป็นรหัส ASCII ของ '7' คือ 55 → `00110111` (= 0x37)

> **สรุป: เลข 7 กับตัวอักษร '7' เก็บในหน่วยความจำไม่เหมือนกัน**

## 1.8 ข้อความ (string) ในภาษาไพธอน

- ตัวอักษรในไพธอนเรียกว่า **ข้อความ (string)** เช่น `"Com"`, `"kmitl"`
- ใช้รหัส ASCII ในการเก็บข้อมูล
- คร่อมด้วย **single quote** `'zebra'` หรือ **double quote** `"Com"`
- ห้ามใช้เครื่องหมายเอียง `‘xx’` , `“xx”` (ใช้ไม่ได้)

## 1.9 คำสั่ง print

```python
print(arg1, arg2, arg3, ...)
```

- `print` คือ **ฟังก์ชัน** (function) — การเรียกใช้ฟังก์ชันจะมีวงเล็บต่อท้ายเสมอ
- สิ่งที่อยู่ในวงเล็บเรียกว่า **อาร์กิวเมนต์ (argument)**
- อาร์กิวเมนต์แต่ละตัวคั่นด้วย **คอมม่า**
- เมื่อทำงานจะ **เว้นช่องว่าง 1 ช่อง** ระหว่างอาร์กิวเมนต์
- เมื่อจบคำสั่งจะ **ขึ้นบรรทัดใหม่อัตโนมัติ**

```python
print(345)                      # 345
print("kmitl")                  # kmitl
print(70,93,45)                 # 70 93 45
print(345, 3.14, "kmitl")       # 345 3.14 kmitl
print("kmitl\nBangkok")         # kmitl (ขึ้นบรรทัดใหม่) Bangkok
```

### รูปแบบเต็มของ print

```python
print(arg1, arg2, ..., sep=" ", end="\n")
```

| ตัวอย่าง | ผลลัพธ์ |
|---|---|
| `print(1,2,3,4,5)` | `1 2 3 4 5` |
| `print(1,2,3,4,5,sep="")` | `12345` |
| `print(1,2,3,4,5,sep="x")` | `1x2x3x4x5` |
| `print("A", end="")` | พิมพ์ `A` แล้ว **ไม่ขึ้นบรรทัดใหม่** |

## 1.10 คำอธิบายโปรแกรม (comment)

- ใช้สัญลักษณ์ `#`
- จากตำแหน่งนั้นไปจนจบบรรทัดจะ **ไม่มีผลต่อการทำงาน**
- ต้องไม่เป็นส่วนหนึ่งของข้อความ (string)
- ใช้เพื่ออธิบายโปรแกรม / ใช้เพื่อ debug
- สามารถใช้ **docstrings** ได้ (`'''` , `"""`) — triple quote มีได้หลายบรรทัด

---

# บทที่ 2 ตัวแปร นิพจน์ คำสั่งรับข้อมูลและแสดงผล

## 2.1 ตัวแปร (Variables)

- ตัวแปรเป็น **ชื่อสำหรับเรียกหน่วยความจำ**
- หน้าที่ 2 แบบ: **เก็บข้อมูล (store)** และ **นำไปใช้งาน (retrieve)**
- สร้างตัวแปรโดยใช้เครื่องหมาย `=` เรียกว่า **Assignment operator**
- ตัวแปรมีชนิดข้อมูล (data type): `str`, `int`, `float`, `bool`

```python
x = 12.2
y = 14
z = "Hello"
```

### กฎการตั้งชื่อตัวแปร ⭐

1. ต้องไม่เป็น **คำสงวน (reserved word)**
2. อักขระตัวแรกต้องเป็น **อักษรภาษาอังกฤษ หรือ `_` (underscore)** — ห้ามขึ้นต้นด้วยตัวเลข
3. อักขระตัวถัดไปมีตัวเลขได้
4. **ห้ามมีช่องว่าง** ภายในชื่อ
5. ตัวพิมพ์ใหญ่-เล็กเป็นคนละชื่อกัน (**case sensitive**) — `myname`, `MyName`, `myName`, `mynamE` แตกต่างกันหมด
6. ควรตั้งชื่อให้มีความหมาย และตัวแปรปกติควรใช้อักษรตัวเล็ก

### คำสงวน (Reserved word) ในภาษาไพธอน

```
False   None    True    and     as      assert  break
class   continue def    del     elif    else    except
finally for     from    global  if      import  in
is      lambda  nonlocal not    or      pass    raise
return  try     while   with    yield
```
> Hint: ใน VScode คำสงวนจะเป็น **สีม่วง**

### ตัวอย่างการตั้งชื่อ

| ✅ ถูกต้อง | ❌ ผิด | เหตุผลที่ผิด |
|---|---|---|
| `_money = 99.25` | `$money = 14.125` | ขึ้นต้นด้วย `$` |
| `num = 191` | `lambda = 2.7` | เป็นคำสงวน |
| `my_name = "John"` | `my-name = "Elizabeth"` | มีเครื่องหมาย `-` |
| `name2 = 'Luke'` | `First name = "John"` | มีช่องว่าง |
| `area = 4*5` | `percent% = 60` | มีเครื่องหมาย `%` |
| `income = 25_000_67` | `V1.5 = 23` | มีจุด และขึ้นต้นเป็นเลขหลังจุด |
| `addr = 0x64ab_41CE` | `num = 017` | เลขนำหน้าเป็น 0 |
| `x = 0b_1101_0111` | | |

> `0b...` = เลขฐานสอง, `0x...` = เลขฐานสิบหก, `_` ในตัวเลขใช้คั่นให้อ่านง่าย

### ตั้งชื่อไม่เหมาะสม vs เหมาะสม
```python
x1q3z9ocd = 35.0            #  อ่านไม่รู้เรื่อง
x1q3z9afd = 12.50
x1q3p9afd = x1q3z9ocd * x1q3z9afd

width  = 35.0               #  สื่อความหมาย
height = 12.50
area   = width * height     # area = 437.5
```

## 2.2 ชนิดข้อมูล (Data type)

| ชนิด | เก็บอะไร |
|---|---|
| `str` (string) | ข้อความ |
| `int` | จำนวนเต็ม |
| `float` | ทศนิยม |
| `bool` | `True` / `False` |

- ตรวจสอบชนิดข้อมูลด้วยฟังก์ชัน **`type()`**

```python
str1 = "Hello1"
print(type(str1))     # <class 'str'>
```

## 2.3 ตัวแปรชนิดข้อความ (string)

- คร่อมด้วย single quote `'` หรือ double quote `"`
- **ไม่ใช่** เครื่องหมายเอียง `‘ ’` หรือ `“ ”`
- คร่อมด้วย `'` ใส่ `"` ข้างในได้ / คร่อมด้วย `"` ใส่ `'` ข้างในได้
- หรือใช้ **escape character** เช่น `\n` (ขึ้นบรรทัดใหม่), `\t` (แท็บ), `\\` (backslash)

## 2.4 การจัดรูปแบบด้วย f-string ⭐⭐ (ออกสอบแน่)

```python
str1, str2 = "Hello", 'Linda'
print(f"line1 --{str1} {str2}--")   # line1 --Hello Linda--
print(f"line2 --{str1+str2}--")     # line2 --HelloLinda--
print(f"line3 --{str1:10s}--")      # line3 --Hello     --   (จอง 10 ช่อง ชิดซ้าย)
print(f"line4 --{str1:^10s}--")     # line4 --  Hello   --   (กึ่งกลาง)
print(f"line5 --{str1:<10s}--")     # line5 --Hello     --   (ชิดซ้าย)
print(f"line6 --{str1:>10s}--")     # line6 --     Hello--   (ชิดขวา)
print(f"line7 --{str1*2}--")        # line7 --HelloHello--
```

### สรุปสัญลักษณ์จัดรูปแบบ

| สัญลักษณ์ | ความหมาย |
|---|---|
| `<` | ชิดซ้าย |
| `>` | ชิดขวา |
| `^` | กึ่งกลาง |
| `d` | เลขฐานสิบ (decimal) |
| `b` | เลขฐานสอง (binary) |
| `x` / `X` | เลขฐานสิบหก ตัวพิมพ์เล็ก / ใหญ่ |
| `f` | ทศนิยม (float) |
| `s` | ข้อความ (string) |
| `,` | ใส่คอมม่าคั่นหลักพัน |
| `0` นำหน้า | เติมศูนย์ข้างหน้า |

> **สำคัญ:** `{x:f}` ถ้าไม่ระบุจำนวนทศนิยม จะแสดง **6 ตำแหน่ง** เสมอ

### ตัวอย่างจำนวนเต็ม
```python
x = 123
print(f"{x:5d}")     # "  123"   จอง 5 ช่อง ชิดขวา (default ของตัวเลข)
print(f"{x:<5d}")    # "123  "
print(f"{x:>5d}")    # "  123"
print(f"{x:^5d}")    # " 123 "
print(f"{x*5000:,}") # 615,000
```

### เลขฐาน 16 / ฐาน 2
```python
x = 0x7f                     # = 127
print(f"{x:5x}")             # "   7f"
x = 0x10cb                   # = 4299
print(f"{x:8X}")             # "    10CB"
x = 127
print(f"{x:12b}")            # "     1111111"
```

### แสดงผลแบบมีศูนย์นำหน้า
```python
num = 30
print(f"{num:08d}")   # 00000030
print(f"{num:08x}")   # 0000001e
print(f"{num:08X}")   # 0000001E
print(f"{num:08b}")   # 00011110
```

### ทศนิยม (float)
```python
x = 12.25
print(f"{x:0.2f}")    # 12.25
print(f"{x:0.8f}")    # 12.25000000
print(f"{x:10.3f}")   # "    12.250"
print(f"{x:10.0f}")   # "        12"

x = 1024.25
print(f"{x:,}")       # 1,024.25
print(f"{x:f}")       # 1024.250000    ← ไม่ระบุ = 6 ตำแหน่ง
print(f"{x:,f}")      # 1,024.250000
print(f"{x:0.1f}")    # 1024.2
```

```python
x = 1.25e3            # = 1250.0 (ชนิด float)
```

## 2.5 เครื่องหมายคำนวณทางคณิตศาสตร์ ⭐⭐

| เครื่องหมาย | การทำงาน | ตัวอย่าง | ผลลัพธ์ |
|---|---|---|---|
| `+` | บวก | `print(5+3)` | `8` |
| `-` | ลบ | `print(5-3)` | `2` |
| `*` | คูณ | `print(5*3)` | `15` |
| `/` | หาร (classic) — **ได้ float เสมอ** | `print(35/7)` | `5.0` |
| `%` | เศษจากการหาร (mod) | `print(39%7)` | `4` |
| `//` | หารปัดเศษลง (floor) | `print(35//9)` | `3` |
| `**` | ยกกำลัง | `print(2**10)` | `1024` |

**เคสสำคัญที่มักออกสอบ**

```python
print(5/3)          # 1.6666666666666667
print(39 % -7)      # -3      ← เครื่องหมายตามตัวหาร
print(35.0 % 7)     # 0.0     ← มี float ปน ผลเป็น float
print(35.5 // 9)    # 3.0     ← มี float ปน ผลเป็น float
print(4 ** 0.5)     # 2.0     ← รากที่สอง
```

### เครื่องหมายแบบลดรูป

| ลดรูป | รูปแบบเต็ม |
|---|---|
| `y += x` | `y = y + x` |
| `y -= x` | `y = y - x` |
| `y *= x` | `y = y * x` |
| `y /= x` | `y = y / x` |
| `y %= x` | `y = y % x` |
| `y //= x` | `y = y // x` |
| `y **= x` | `y = y ** x` |

## 2.6 ลำดับการดำเนินการ (Operator precedence) ⭐⭐

| ลำดับ | เครื่องหมาย |
|---|---|
| 1 | `()` วงเล็บ |
| 2 | `**` (ทำจาก **ขวามาซ้าย**) |
| 3 | `*`, `/`, `//`, `%` (ซ้ายมาขวา) |
| 4 | `+`, `-` |
| 5 | `<`, `<=`, `>`, `>=`, `==`, `!=`, `is`, `is not`, `in`, `not in` |
| 6 | `not` |
| 7 | `and` |
| 8 | `or` |
| 9 | `*=`, `/=`, `%=`, `+=`, `-=` |

### ตัวอย่างการประเมินผลนิพจน์

```
6 + 3 * (2+1)  →  6 + 3*3  →  6 + 9  →  15
17.5 * (9-6) ** 2  →  17.5 * 3**2  →  17.5 * 9  →  157.5
```

### ตารางฝึกที่ต้องจำ ⭐

| นิพจน์ | ผลลัพธ์ | นิพจน์ | ผลลัพธ์ |
|---|---|---|---|
| `(2+3)*4` | `20` | `24/6//2` | `2.0` |
| `2+3*4` | `14` | `24//6//2` | `2` |
| `2**2**3` | `256` | `4+18/3-1` | `9.0` |
| `(2**2)**3` | `64` | `4+18//3-1` | `9` |
| `10//3*2` | `6` | `15%4*7` | `21` |
| `10//(3*2)` | `1` | `8*2%5` | `1` |
| `20//2**3` | `2` | `15/4%5` | `3.75` |
| `(20//2)**3` | `1000` | `15//4%5` | `3` |
| `2**-1` | `0.5` | `10%(4*3)` | `10` |

> **จำ:** `2**2**3` = `2**(2**3)` = `2**8` = 256 (ไม่ใช่ 64) เพราะ `**` ทำจากขวามาซ้าย

ตัวอย่างยาว:
```
-10/5 - 2*6 + (3+4)**(-7+9) + 8 - 1
= -10/5 - 2*6 + 7**2 + 8 - 1
= -2.0 - 12 + 49 + 8 - 1
= 42.0
```

## 2.7 การรับข้อมูล — ฟังก์ชัน `input()` ⭐⭐

```python
x = input("Enter something : ")
print(x, type(x))
```
```
Enter something : 706
706 <class 'str'>
```

> **ข้อมูลที่รับเข้ามาด้วย `input()` จะเป็น string เสมอ** ไม่ว่าจะพิมพ์ตัวเลขก็ตาม

### รับ input หลายจำนวนด้วย `.split()`

```python
m = input("Enter x y : ")     # ผู้ใช้พิมพ์ 5 7
x, y = m.split()
print(x, type(x))             # 5 <class 'str'>
print(y, type(y))             # 7 <class 'str'>
```

- `.split()` เป็น **method** (ไม่ใช่ function) ใช้ตัดข้อความด้วยช่องว่าง
- ถ้าคั่นด้วยตัวอื่น เช่น `1,2` ให้ใช้ `.split(",")`
- ถ้ารับค่าเดียวโดยไม่แยกตัวแปร จะได้ **list** เช่น
  ```python
  x = input().split()     # input: 1 2 3 4 5
  print(x)                # ['1', '2', '3', '4', '5']
  ```

## 2.8 การแปลงชนิดข้อมูล (Casting / Type conversion) ⭐

```python
age    = int(age)        # ข้อความ → จำนวนเต็ม
height = float(height)   # ข้อความ → ทศนิยม
s      = str(x)          # ตัวเลข  → ข้อความ
```

```python
x = int(1)        # 1
y = int(2.8)      # 2   ← ตัดทศนิยมทิ้ง
z = int("3")      # 3
x = float(1)      # 1.0
w = float("4.2")  # 4.2
y = str(2)        # "2"
```

### เปลี่ยนตัวเลขเป็นข้อความแบบจัดรูปแบบ
```python
x = 3.1415926
s = str(x)              # '3.1415926'   <class 'str'>
s = f"{x:0.6f}"         # '3.141593'
s = f"{x*10000:,.3f}"   # '31,415.926'
```

---

# บทที่ 3 การเขียนโปรแกรมแบบมีเงื่อนไข (Conditional Execution)

## 3.1 Boolean expression และเครื่องหมายเปรียบเทียบ ⭐

**Boolean expression** คือนิพจน์ที่ถามคำถามและให้ผลลัพธ์ **True / False** ใช้ควบคุมทิศทางโปรแกรม
เครื่องหมายเปรียบเทียบ **ดูค่าตัวแปร แต่ไม่เปลี่ยนค่าตัวแปร**

| Python | ความหมาย |
|---|---|
| `<` | น้อยกว่า |
| `<=` | น้อยกว่าหรือเท่ากับ |
| `==` | **เท่ากับ** |
| `>=` | มากกว่าหรือเท่ากับ |
| `>` | มากกว่า |
| `!=` | ไม่เท่ากับ |

> ⚠️ `=` ใช้ **กำหนดค่า (assignment)** ส่วน `==` ใช้ **เปรียบเทียบ** — คนละอย่างกัน

### ตัวอย่างผลการเปรียบเทียบ

| นิพจน์ | ผล | นิพจน์ | ผล |
|---|---|---|---|
| `7 == 9` | False | `22 == 22` | True |
| `7 != 9` | True | `(3+5) != 8` | False |
| `8 > 8` | False | `9 > 7` | True |
| `8 >= 8` | True | `7 >= 9` | False |
| `(10+9) < 7` | False | `7 < (10+9)` | True |
| `4 <= 3` | False | **`0.1+0.2 == 0.3`** | **False** ⭐ |

> ⭐ **ห้ามใช้ `==` หรือ `!=` กับข้อมูลทศนิยม (float)** เพราะมี error จากการเก็บค่าในเครื่อง
> `0.1+0.2` ได้ `0.30000000000000004` ไม่เท่ากับ `0.3`

## 3.2 One-Way Decision (if เดี่ยว)

```python
x = 5
print('Before 5')
if x == 5 :
    print('Is 5')
    print('Is Still 5')
    print('Third 5')
print('Afterwards 5')
print('Before 6')
if x == 6 :
    print('Is 6')
print('Afterwards 6')
```
ผลลัพธ์: `Before 5 / Is 5 / Is Still 5 / Third 5 / Afterwards 5 / Before 6 / Afterwards 6`
(บล็อกของ `if x == 6` ไม่ทำงานเลย)

## 3.3 การย่อหน้า (Indentation) ⭐⭐ — หัวใจของ Python

- **เพิ่ม** ย่อหน้าหลังคำสั่ง `if` หรือ `for` (หลังเครื่องหมาย `:` )
- **รักษา** ย่อหน้าเท่าเดิม เพื่อบอกขอบเขต (scope) ของบล็อก
- **ลด** ย่อหน้ากลับมาระดับเดิม เพื่อบอกจุดจบของบล็อก
- **บรรทัดว่างถูกละเว้น** ไม่มีผลต่อ indentation
- **comment บรรทัดเดียว** ก็ถูกละเว้นเช่นกัน
- **หลีกเลี่ยงการใช้ Tab** (ปนกับ space จะพัง) → แนะนำ **4 spaces**

```python
x = 5
if x > 2 :
    print('Bigger than 2')       # อยู่ในบล็อก if
    print('Still bigger')        # อยู่ในบล็อก if
print('Done with 2')             # นอกบล็อก ทำงานเสมอ
```

## 3.4 Two-Way Decision (if / else)

```python
x = 4
if x > 2 :
    print('Bigger')
else :
    print('Smaller')
print('All done')
```
> เหมือนทางแยก: ต้องเลือกทางใดทางหนึ่ง **ไม่ทำทั้งสองทาง**

## 3.5 Nested Decisions (if ซ้อน if)

```python
x = 42
if x > 1 :
    print('More than one')
    if x < 100 :
        print('Less than 100')
print('All done')
```

## 3.6 Multi-way Decision (if / elif / else) ⭐

```python
x = 5
if x < 2 :
    print('small')
elif x < 10 :
    print('Medium')
else :
    print('LARGE')
print('All done')
```

| ค่า x | ผลลัพธ์ |
|---|---|
| 0 | small |
| 5 | Medium |
| 20 | LARGE |

- `elif` ใส่กี่อันก็ได้
- **`else` ไม่จำเป็นต้องมี** (ถ้าไม่มีและไม่ตรงเงื่อนไขใดเลย จะไม่ทำอะไร)
- โปรแกรมจะเช็คจาก **บนลงล่าง** เจอเงื่อนไขจริงอันแรกแล้ว **ออกจากโครงสร้างทันที**

### Multi-way Puzzles ⭐⭐ (ข้อสอบชอบถาม)

**ชุดที่ 1** — บรรทัดไหนไม่มีวันพิมพ์?
```python
if x < 2 :
    print('Below 2')
elif x >= 2 :
    print('Two or more')
else :
    print('Something else')      # ← ไม่มีวันพิมพ์ (สองเงื่อนไขบนครอบคลุมทุกกรณี)
```

**ชุดที่ 2**
```python
if x < 2 :
    print('Below 2')
elif x < 20 :
    print('Below 20')
elif x < 10 :
    print('Below 10')            # ← ไม่มีวันพิมพ์ (ถ้า x<10 ก็ติด x<20 ไปก่อนแล้ว)
else :
    print('Something else')
```

## 3.7 try / except ⭐

- ครอบโค้ดที่ "อันตราย" (อาจ error) ไว้ใน `try`
- ถ้าโค้ดใน `try` **ทำงานสำเร็จ** → **ข้าม** `except`
- ถ้าโค้ดใน `try` **ผิดพลาด** → **กระโดดไปทำ** `except` แล้วโปรแกรมทำงานต่อ (ไม่พัง)
- ส่วนใหญ่ใช้เช็ค type ของค่าว่าแปลงเป็น int / float ได้หรือไม่

```python
astr = 'Hello Bob'
try:
    istr = int(astr)
except:
    istr = -1
print('First', istr)      # First -1

astr = '123'
try:
    istr = int(astr)
except:
    istr = -1
print('Second', istr)     # Second 123
```

> ⚠️ ถ้าเกิด error กลางบล็อก `try` **คำสั่งที่เหลือในบล็อก `try` จะไม่ถูกทำงาน**
> ```python
> astr = 'Bob'
> try:
>     print('Hello')
>     istr = int(astr)      # error ที่บรรทัดนี้
>     print('There')        # ← ไม่ถูกพิมพ์
> except:
>     istr = -1
> print('Done', istr)       # Hello / Done -1
> ```

ตัวอย่างใช้งานจริง:
```python
rawstr = input('Enter a number:')
try:
    ival = int(rawstr)
except:
    ival = -1

if ival > 0 :
    print('Nice work')
else:
    print('Not a number')
```

## 3.8 ตัวดำเนินการทางตรรกศาสตร์ (Logical operators) ⭐

| เครื่องหมาย | ความหมาย | ตัวอย่าง |
|---|---|---|
| `and` | และ | `x and y` |
| `or` | หรือ | `x or y` |
| `not` | ไม่ / ตรงกันข้าม | `not x` |

### ตารางค่าความจริง

| A | B | A and B | A or B |
|---|---|---|---|
| T | T | **T** | **T** |
| T | F | F | **T** |
| F | T | F | **T** |
| F | F | F | F |

| A | not A |
|---|---|
| T | F |
| F | T |

### ตัวอย่าง
```python
num1, num2, num3 = 10, 20, 30

num1 == num2                      # False
num1 > num2                       # False
(num1<num2) and (num2<num3)       # True
(num1>num2) or  (num1>num3)       # False
(num1>num2) or  (num2<num3)       # True
```

## 3.9 ตัวอย่างโปรแกรมสำคัญ

### โปรแกรมหารเลข 2 จำนวน (ตรวจตัวหารเป็นศูนย์)
```python
astr = input("Enter num1 num2 : ")
num1, num2 = astr.split()
num1 = int(num1)
num2 = int(num2)
if num2 == 0:
    print("Error divided by zero")
else:
    print(f"{num1} / {num2} = {num1/num2}")
```
```
Enter num1 num2 : 2 0
Error divided by zero
Enter num1 num2 : 3 5
3 / 5 = 0.6
```

### โปรแกรมตัดเกรด (if / elif) ⭐
เกณฑ์: 82–100 = A, 68–81.99 = B, 54–67.99 = C, 40–53.99 = D, 0–39.99 = F

```python
astr = input("Enter name score : ")
name, score = astr.split()
score = float(score)
if score >= 82:
    grade = 'A'
elif score >= 68:
    grade = 'B'
elif score >= 54:
    grade = 'C'
elif score >= 40:
    grade = 'D'
else:
    grade = 'F'
print(f"{name} got {score:.2f} and {grade} grade !!!")
```
```
Enter name score : Linda 88     →  Linda got 88.00 and A grade !!!
Enter name score : Jim 55.5     →  Jim got 55.50 and C grade !!!
Enter name score : Aura 39.99   →  Aura got 39.99 and F grade !!!
```

### ตรวจว่าผลหารเป็นจำนวนเต็มหรือไม่
```python
x = 30/2
if int(x) == x :                        # หรือใช้  if x % 1 == 0 :
    print(f"{int(x)} is an integer.")   # 15 is an integer.
else:
    print(f"{x} is a float.")

x = 100/32                              # 3.125 is a float.
```

---

# บทที่ 4 การเขียนโปรแกรมแบบวนซ้ำ (while)

## 4.1 หลักการของ while — Indefinite Loop

```python
n = 5
while n > 0 :
    print(n)
    n = n - 1
print('Blastoff!')
print(n)
```
ผลลัพธ์: `5 4 3 2 1 Blastoff! 0`

- Loop มี **ตัวแปรควบคุมการวน (iteration variable)** ที่เปลี่ยนค่าทุกรอบ
- while เรียกว่า **indefinite loop** เพราะไม่รู้ล่วงหน้าว่าจะวนกี่รอบ
- **3 สิ่งที่ต้องมีเสมอ:** กำหนดค่าเริ่มต้น → เงื่อนไข → **เปลี่ยนค่าตัวแปรควบคุมในลูป**

## 4.2 Infinite Loop และ Loop ที่ไม่ทำงานเลย ⭐

**วนไม่รู้จบ** — ลืมเปลี่ยนค่า `n`
```python
n = 5
while n > 0 :
    print('Lather')
    print('Rinse')
print('Dry off!')       # ← ไม่มีวันถึงบรรทัดนี้
```

**ไม่ทำงานเลยสักรอบ** — เงื่อนไขเป็นเท็จตั้งแต่แรก
```python
n = 0
while n > 0 :
    print('Lather')
print('Dry off!')       # พิมพ์ Dry off! อย่างเดียว
```

## 4.3 ตัวอย่างโปรแกรม while

### แสดงเลข 0–10
```python
print(" *** Show number 0 to 10 ***")
count = 0
while count <= 10:
    print(f"{count} ", end="")
    count += 1
print("\n===== End of Program =====")
```
```
*** Show number 0 to 10 ***
0 1 2 3 4 5 6 7 8 9 10
===== End of Program =====
```
> วนทั้งหมด **11 รอบ** (0 ถึง 10) และเช็คเงื่อนไข **12 ครั้ง**

### หาผลรวม 1 ถึง n
```python
n = int(input("Enter n : "))
sum = 0
i = 1
while i <= n:
    sum += i
    i += 1
print(f"Summation from 1 to {n} = {sum:,d}")
```
```
Enter n : 48
Summation from 1 to 48 = 1,176
```

## 4.4 break และ continue ⭐⭐

| คำสั่ง | การทำงาน |
|---|---|
| **`break`** | **จบลูปทันที** แล้วกระโดดไปทำคำสั่งถัดจากลูป |
| **`continue`** | **จบรอบปัจจุบัน** แล้วกระโดดกลับไปเริ่มรอบถัดไปทันที (บรรทัดที่เหลือในลูปไม่ทำงาน) |

```python
while True:                     # ← ลูปไม่รู้จบ ต้องมี break
    line = input('> ')
    if line == 'done' :
        break
    print(line)
print('Done!')
```

```python
while True:
    line = input('> ')
    if line[0] == '#' :
        continue                # ข้ามบรรทัดที่ขึ้นต้นด้วย #
    if line == 'done' :
        break
    print(line)
print('Done!')
```

ตัวอย่างจาก cheat sheet:
```python
a = 10
while a > 0:
    a -= 1
    if a == 5:
        continue
    print(a, end=" ")
# output : 9 8 7 6 4 3 2 1 0      ← ไม่มี 5
```

## 4.5 ฟังก์ชัน `ord()` และ `chr()` ⭐

| ฟังก์ชัน | ทำอะไร |
|---|---|
| `ord(ch)` | แปลง **ตัวอักษร 1 ตัว** → รหัส ASCII (ตัวเลข) |
| `chr(num)` | แปลง **รหัส ASCII** → ตัวอักษร |

```python
print(ord("A"))      # 65   (= 0x41)
print(ord("a"))      # 97
print(chr(97))       # a
print(chr(97+2))     # c
```

> ⚠️ `ord()` รับได้แค่ **ตัวอักษรตัวเดียว** — `ord("Abx")` จะเกิด
> `TypeError: ord() expected a character, but string of length 3 found`

### แสดงตัวอักษร a–z ด้วย while
```python
i = 0
while i < 26:
    num  = ord("a") + i
    char = chr(num)
    print(f"{char} ", end="")
    i += 1
```

## 4.6 `len()` และการเข้าถึงตัวอักษรใน string (String subscript) ⭐

- `len(s)` = ความยาวของ string เช่น `len("abcd")` = 4
- `name[i]` = ตัวอักษรตำแหน่งที่ i (**เริ่มนับจาก 0**)

```python
name = "Python creator: Gudio van Rossum"
length = len(name)          # 32
i = 0
while i < length:
    print(name[i], end="")
    i += 1
```

```python
name[0] = 'P' = 0x50 = 0080
name[1] = 'y' = 0x79 = 0121
name[2] = 't' = 0x74 = 0116
```

## 4.7 Nested Loop (ลูปซ้อนลูป) ⭐⭐

### วาดสี่เหลี่ยม
```python
num = int(input("Enter size : "))
row = 0
ch  = "*"
while row < num :
    col = 0
    while col < num :
        print(f"{ch}", end="")
        col += 1
    print()                     # ขึ้นบรรทัดใหม่เมื่อจบแถว
    row += 1
```
> ลูปนอกคุม **แถว (row)**, ลูปในคุม **คอลัมน์ (col)** — ทำงานทั้งหมด `num × num` รอบ

### สี่เหลี่ยมสลับ `$` กับ `=`
```python
while row < num :
    col = 0
    while col < num :
        if (row+col) % 2 == 0 :
            ch = "$"
        else :
            ch = "="
        print(f"{ch}", end="")
        col += 1
    print()
    row += 1
```
```
$=$=$
=$=$=
$=$=$
```

### พีระมิด ⭐ (สูตรที่ต้องจำ)

```
row 0 :  ช่องว่าง 4  ดาว 1
row 1 :  ช่องว่าง 3  ดาว 3
row 2 :  ช่องว่าง 2  ดาว 5
```

> **จำนวนช่องว่าง = `num - row - 1`  |  จำนวนดาว = `2*row + 1`  |  ความกว้างรวม = `2*num - 1`**

แบบที่ 1 (เช็คเงื่อนไขทีละช่อง):
```python
while row < num :
    col = 0
    while col < 2*num-1 :
        if (row+col >= num-1) and col < (row + num) :
            ch = "*"
        else :
            ch = " "
        print(f"{ch}", end="")
        col += 1
    print()
    row += 1
```

แบบที่ 2 (ใช้การคูณ string — สั้นกว่า):
```python
space = ' '
star  = '*'
row = 0
while row < num :
    line  = space * (num-row-1)
    line += star  * (2*row+1)
    print(line)
    row += 1
```

## สรุปหัวข้อบทที่ 4
`while loop (indefinite)` • `infinite loop` • `iteration variable` • `break` • `continue` • `len()` • `ord()` • `chr()` • `string subscript` • `nested loop`

---

# บทที่ 5 การเขียนโปรแกรมแบบวนซ้ำ (for)

## 5.1 Definite Loop

- `for` เรียกว่า **definite loop** เพราะรู้จำนวนรอบแน่นอน = จำนวนสมาชิกในชุดข้อมูล
- "definite loops iterate through the members of a set"

```python
for i in [5, 4, 3, 2, 1] :
    print(i)
print('Blastoff!')
# 5 4 3 2 1 Blastoff!
```

```python
friends = ['Joseph', 'Glenn', 'Sally']
for friend in friends :
    print('Happy New Year:', friend)
print('Done!')
```

- **ตัวแปรวนรอบ (iteration variable)** จะไล่ค่าไปทีละตัวตามลำดับในชุดข้อมูล
- บล็อกในลูปทำงาน **1 ครั้งต่อ 1 สมาชิก**

## 5.2 ฟังก์ชัน `range()` ⭐⭐

```python
range(start, stop, step)
```
- ได้ค่าตั้งแต่ `start` ถึง `stop - 1` (**ไม่รวม stop**)
- ใส่ argument เดียว = `stop` (เริ่มที่ 0)
- `step` เป็นลบได้ = นับถอยหลัง

| คำสั่ง | ค่าที่ได้ |
|---|---|
| `range(5)` | `0 1 2 3 4` |
| `range(10)` | `0 1 2 3 4 5 6 7 8 9` |
| `range(3,9)` | `3 4 5 6 7 8` |
| `range(3,9,2)` | `3 5 7` |
| `range(13,5,-2)` | `13 11 9 7` |

## 5.3 Loop Idioms — รูปแบบการใช้ลูปที่ต้องจำ ⭐⭐⭐

> หลักการ: **ตั้งค่าตัวแปรเริ่มต้น → วนลูปดู/ทำกับแต่ละตัวและอัปเดตตัวแปร → ดูค่าตัวแปรตอนจบ**

ชุดข้อมูลตัวอย่าง: `[9, 41, 12, 3, 74, 15]`

### (1) หาค่ามากที่สุด (Largest)
```python
largest_so_far = -1
for the_num in [9, 41, 12, 3, 74, 15] :
    if the_num > largest_so_far :
        largest_so_far = the_num
print('After', largest_so_far)      # After 74
```

### (2) นับจำนวนรอบ (Counting)
```python
zork = 0
for thing in [9, 41, 12, 3, 74, 15] :
    zork = zork + 1
print('After', zork)                # After 6
```

### (3) หาผลรวม (Summing)
```python
zork = 0
for thing in [9, 41, 12, 3, 74, 15] :
    zork = zork + thing
print('After', zork)                # After 154
```

### (4) หาค่าเฉลี่ย (Average) = นับ + รวม แล้วหารตอนจบ
```python
count = 0
sum = 0
for value in [9, 41, 12, 3, 74, 15] :
    count = count + 1
    sum = sum + value
print('After', count, sum, sum/count)   # After 6 154 25.666666666666668
```

### (5) กรองข้อมูล (Filtering) — ใช้ `if` ในลูป
```python
for value in [9, 41, 12, 3, 74, 15] :
    if value > 20:
        print('Large number', value)
# Large number 41
# Large number 74
```

### (6) ค้นหาด้วยตัวแปร Boolean (Search)
```python
found = False
for value in [9, 41, 12, 3, 74, 15] :
    if value == 3 :
        found = True
print('After', found)               # After True
```

### (7) หาค่าน้อยที่สุด (Smallest) ⭐ กับดักข้อสอบ

**ผิด!** — แค่เปลี่ยน `>` เป็น `<` โดยยังใช้ค่าเริ่มต้น `-1`
```python
smallest_so_far = -1
for the_num in [9, 41, 12, 3, 74, 15] :
    if the_num < smallest_so_far :
        smallest_so_far = the_num
print('After', smallest_so_far)     # After -1   ← ผิด!
```

**ถูก** — ใช้ `None` เป็นค่าเริ่มต้น
```python
smallest = None
for value in [9, 41, 12, 3, 74, 15] :
    if smallest is None :
        smallest = value
    elif value < smallest :
        smallest = value
print('After', smallest)            # After 3
```

## 5.4 ตัวดำเนินการ `is` และ `is not`

- `is` แปลว่า **"เป็นตัวเดียวกันกับ"** (is the same as)
- คล้าย `==` แต่ **เข้มงวดกว่า** (เทียบว่าเป็นวัตถุเดียวกันในหน่วยความจำ)
- ใช้คู่กับ `None` เสมอ เช่น `if smallest is None :`
- `is not` เป็น logical operator เช่นกัน

## 5.5 ตัวอย่างโปรแกรม for

### แสดง a–z
```python
print(" *** Show Alphabet ***")
for i in range(26):
    num  = ord("a") + i
    char = chr(num)
    print(f"{char} ", end="")
print("\n===== End of Program =====")
```

### วน for กับผลของ `split()`
```python
words = input("Enter words : ")      # hello there
count = 0
for word in words.split():
    print(f"{word} ", sep="=", end="=")
    count += 1
print("\ncount =", count)
# hello=there=
# count = 2
```

### วน for กับ string (ทีละตัวอักษร)
```python
message = "Let's party !!!"
n = 1
for x in message:
    print(f"{n}={x}", end=" ")
    n += 1
# 1=L 2=e 3=t 4=' 5=s 6=  7=p 8=a 9=r 10=t 11=y 12=  13=! 14=! 15=!
```

### พีระมิดด้วย for (หลายเวอร์ชัน)
```python
# v-02 : สั้นที่สุด
num = int(input("Enter height : "))
for row in range(num):
    line  = ' '*(num-row-1)
    line += '*'*(2*row+1)
    print(line)

# v-05 : บรรทัดเดียว
for row in range(num):
    print(f"{' '*(num-row-1)}{'*'*(2*row+1)}")

# แบบ nested for
for row in range(num):
    for col in range(row+num):
        if row+col < num-1:
            print(' ', end="")
        else:
            print('*', end="")
    print()
```

### พีระมิดตัวเลข 0–9
```python
num = int(input("Enter height : "))
n = 0
for row in range(num):
    line = ' '*(num-row-1)
    for ch in range(2*row+1):
        line += str(n % 10)
        n += 1
    print(line)
```
```
Enter height : 5
    0
   123
  45678
 9012345
678901234
```

## 5.6 `in` ใช้ตรวจสมาชิก

```python
message = "hello"
word = "aeiou"
for letter in message:
    if letter in word :
        print("vowel", end="")
# output : vowelvowel   (e และ o)
```

## สรุปหัวข้อบทที่ 5
`range()` • `for loop (definite)` • `iteration variable` • `loop idioms` • `largest / smallest` • `None` และ `is` • `in str` • `in str.split()`

---

## เปรียบเทียบ while กับ for ⭐

| หัวข้อ | `while` | `for` |
|---|---|---|
| ประเภท | Indefinite loop | **Definite loop** |
| รู้จำนวนรอบล่วงหน้า | ไม่รู้ | รู้ (เท่าจำนวนสมาชิก) |
| ตัวแปรวนรอบ | ต้องกำหนด/เพิ่มค่าเอง | เปลี่ยนให้อัตโนมัติ |
| เสี่ยง infinite loop | **เสี่ยง** (ถ้าลืมเปลี่ยนค่า) | ไม่เสี่ยง |
| ใช้กับ | เงื่อนไขที่ไม่รู้รอบ เช่น รับ input จนกว่าจะพิมพ์ done | ชุดข้อมูล, `range()`, string, list |

---

# ภาคผนวก: เนื้อหาเพิ่มเติมจาก Cheat sheet

## A. List (ลิสต์)

### การสร้าง
```python
stuff  = []                                   # ลิสต์ว่าง
things = list()                               # ลิสต์ว่าง
fruits = "apple mango papaya".split()         # ['apple', 'mango', 'papaya']
friends = ['Joseph', 'Glenn', 'Sally']
```

### วนลูป 2 แบบ
```python
for friend in friends :                       # วนที่ตัวสมาชิก
    print('Happy New Year:', friend)

for i in range(len(friends)) :                # วนที่ index
    friend = friends[i]
    print('Happy New Year:', friend)
```
```python
print(len(friends))                 # 3
print(list(range(len(friends))))    # [0, 1, 2]
```

### Built-in function กับ list
```python
nums = [3, 41, 12, 9, 74, 15]
print(len(nums))    # 6
print(max(nums))    # 74
print(min(nums))    # 3
print(sum(nums))    # 154
```

### การรวม list
```python
a = [1, 2, 3]
b = [4, 5, 6]
c = a + b           # [1, 2, 3, 4, 5, 6]
```

### List Slicing ⭐
```python
t = [9, 41, 12, 3, 74, 15]
t[1:3]     # [41, 12]        ← ไม่รวม index 3
t[:4]      # [9, 41, 12, 3]
t[3:]      # [3, 74, 15]
t[:]       # [9, 41, 12, 3, 74, 15]   (ทั้งหมด)
t[-1]      # 15              ← ตัวสุดท้าย
t[::-1]    # [15, 74, 3, 12, 41, 9]   (กลับด้าน)
```

### List Method ⭐
```python
x = [1,2,3]
x.index(1)      # 0    หา index ของค่า
x.append(4)     # [1, 2, 3, 4]     เพิ่มท้าย
x.remove(2)     # [1, 3, 4]        ลบตามค่า
x.pop()         # คืนค่าตัวสุดท้ายและลบออก
x.clear()       # []               ล้างทั้งหมด
x.insert(0,7)   # แทรกที่ index 0
x.reverse()     # กลับลำดับ
```

### List copy
```python
x = [1,2,3,4,5]
a = x                # อ้างถึงลิสต์เดียวกัน (ไม่ใช่การก๊อป)
a = list(x)          # ก๊อปใหม่
a = x.copy()         # ก๊อปใหม่
```

### List comprehension
```python
s = "1 2 3 4 5".split()          # ['1','2','3','4','5']

x = []                           # แบบธรรมดา
for ele in s:
    x.append(int(ele))

a = [int(m) for m in s]          # แบบ comprehension → [1, 2, 3, 4, 5]
```

## B. String method ที่ควรจำ ⭐

```python
word = "KMItL"
word.lower()          # 'kmitl'
word.upper()          # 'KMITL'
word.capitalize()     # 'Kmitl'      (ตัวแรกใหญ่ ที่เหลือเล็ก)
word.title()          # 'Kmitl'

sep = '-'
sep.join('KMITL')     # 'K-M-I-T-L'

email = 'programming@kmitl.ac.th'
email.startswith('pro')     # True
email.endswith('.ac.th')    # True
email.find('in')            # 8      (ตำแหน่งที่เจอครั้งแรก)
email.count('a')            # 2

'123'.isdigit()       # True     เป็นตัวเลขล้วน
'123'.isalpha()       # False    เป็นตัวอักษรล้วน
'123'.isalnum()       # True     เป็นตัวอักษร/ตัวเลข
'kmitl'.isalpha()     # True

x = 'The quick brown fox jumps over a lazy dog'
x.replace('a','A')    # 'The quick brown fox jumps over A lAzy dog'

line.rstrip()         # ตัดช่องว่าง/'\n' ท้ายบรรทัด
```

## C. format string มี 3 แบบ

```python
# 1. %-format
firstname = 'Rukpong'
print('My name is %s.' % firstname)

# 2. f-Strings  (นิยมที่สุด)
beverage = 'coffee'
print(f'My name is {firstname}. I like a {beverage}.')

# 3. str.format()
favorite = {'beverage':'coffee', 'money':45}
print('The {beverage} is {money} Baht..'.format(**favorite))
```

## D. Function (`def`) ⭐

```python
x = 5
print('Hello')
def print_lyrics():
    print("I'm a lumberjack, and I'm okay.")
    print('I sleep all night and I work all day.')
print('Yo')
print_lyrics()
x = x + 2
print(x)
```
**Output:** `Hello / Yo / I'm a lumberjack... / I sleep all night... / 7`

> ⭐ การ `def` **แค่นิยามฟังก์ชัน ยังไม่ทำงาน** จนกว่าจะถูก **เรียกใช้ (call)**

### Argument กับค่า default
```python
def add4(a, b, c=0, d=99) :
    print(f"a={a} b={b} c={c} d={d}")
    return a+b+c+d

print(add4(3,5,9,8))    # a=3 b=5 c=9 d=8   →  25
print(add4(3,5,9))      # a=3 b=5 c=9 d=99  →  116
print(add4(3,5))        # a=3 b=5 c=0 d=99  →  107
```

### `quit()` — จบโปรแกรมทันที
```python
def print_one():
    print(f"2 - in function x={x}")
    quit()
    print(f"3 - in function x={x}")     # ← ไม่ทำงาน

x = 5
print(f"1 - in main x={x}")
print_one()
print(f"4 - in main x={x}")             # ← ไม่ทำงาน
# OUTPUT: 1 - in main x=5 / 2 - in function x=5
```

## E. Dict (ดิกชันนารี)

Dict คือชุดข้อมูลที่มี **Key** และ **Value** เช่น `{'IDa': 19, 'IDb': 20}`

```python
dict_example = dict()          # หรือ {}
dict_example['IDa'] = 19       # เพิ่มแบบ manual
dict_example['IDb'] = 20

number_of_Book = dict_example.get('Book')     # เข้าถึงค่าด้วย .get()
```

### นับจำนวนด้วย dict ⭐ (แพทเทิร์นสำคัญ)
```python
box = ['Pen', 'Book', 'Pen', 'Pencil']
dict_example = {}
for item in box:
    dict_example[item] = dict_example.get(item, 1) + 1
```
> `.get(key, default)` — ถ้ามี key อยู่แล้วคืนค่าเดิม ถ้าไม่มีคืนค่า default

### เรียงลำดับ dict
```python
d = {'Book': 10, 'Pen': 20, 'Apple': 30}
sorted(d.items())                                  # เรียงตาม key
# [('Apple', 30), ('Book', 10), ('Pen', 20)]
sorted([(v, k) for k, v in d.items()])             # เรียงตาม value
# [(10, 'Book'), (20, 'Pen'), (30, 'Apple')]
```

## F. Tuple

- ลักษณะคล้าย list วิธีเข้าถึงเหมือน list แต่อยู่ในรูป **`( )`**
- **จุดเด่น: ข้อมูลข้างในเปลี่ยนแปลงไม่ได้** (add / update / delete ไม่ได้)

```python
d = {'Book':10, 'Pen':20}
print(d.items())                    # dict_items([('Book',10), ('Pen',20)])
for (key, value) in d.items():
    print(key, value)               # Book 10 / Pen 20
```

## G. File (ไฟล์)

```python
handle = open(filename, mode)      # mode: 'r' = read, 'w' = write
```

### นับบรรทัดในไฟล์
```python
fhand = open(filename)
line_counter = 0
for line in fhand :
    line_counter += 1
```

### ค้นหาคำในไฟล์
```python
fhand = open(filename)
for line in fhand:
    line = line.rstrip()            # ตัด '\n' ออก
    if line.startswith('From'):
        print(line)
```
```python
for line in fhand:
    line = line.rstrip()
    if ' hello ' in line:           # Tip: ใส่ space หน้า-หลัง เพื่อหาคำนั้นตรง ๆ
        print(line)                 #      (กัน 'in' ไปตรงกับ 'sine')
```

### นับจำนวนคำในไฟล์ด้วย dict
```python
fhand = open(filename)
word_counter = {}
for line in fhand:
    words = line.split()
    for word in words:
        word_counter[word] = word_counter.get(word, 1) + 1
```

---

# ✅ Checklist ก่อนเข้าห้องสอบ

**บทที่ 1**
- [ ] แยกฮาร์ดแวร์ 4 ส่วน / ซอฟต์แวร์ระบบ / OS แต่ละตัวและปี
- [ ] Interpreter vs Compiler — Python เป็น interpreter
- [ ] แปลงเลขฐาน 2 ↔ 10 ↔ 16 ได้คล่อง
- [ ] bit / Byte(8bit) / Word(16bit) / KB(2¹⁰) / MB / GB
- [ ] ASCII: 'A'=65=0x41, 'a'=97=0x61, '0'=48 ; เลข 7 ≠ ตัวอักษร '7'

**บทที่ 2**
- [ ] กฎตั้งชื่อตัวแปร + คำสงวน
- [ ] f-string: `<` `>` `^` `d` `b` `x/X` `f` `,` `0`  และ `:f` ไม่ระบุ = 6 ตำแหน่ง
- [ ] `/` ได้ float เสมอ, `//` ปัดลง, `%` เศษ, `**` ขวามาซ้าย
- [ ] ลำดับความสำคัญ: `()` → `**` → `* / // %` → `+ -` → เปรียบเทียบ → `not` → `and` → `or`
- [ ] `input()` คืนค่าเป็น **string เสมอ** → ต้อง `int()` / `float()`
- [ ] `.split()` แยกข้อความ

**บทที่ 3**
- [ ] `=` (กำหนดค่า) vs `==` (เปรียบเทียบ)
- [ ] ห้ามใช้ `==` กับ float (`0.1+0.2 == 0.3` → False)
- [ ] indentation กำหนดขอบเขตบล็อก
- [ ] `if / elif / else` ทำงานบนลงล่าง เจอจริงอันแรกแล้วออก
- [ ] Multi-way puzzle: หา branch ที่ไม่มีวันทำงาน
- [ ] `try / except` — error แล้วโปรแกรมไม่พัง, บรรทัดที่เหลือใน try ถูกข้าม
- [ ] ตาราง `and` / `or` / `not`

**บทที่ 4**
- [ ] while ต้องมีการเปลี่ยนค่าตัวแปรควบคุม ไม่งั้น infinite loop
- [ ] `break` = ออกจากลูป, `continue` = ข้ามไปรอบถัดไป
- [ ] `ord()` / `chr()` / `len()` / `name[i]`
- [ ] nested loop: `num × num` รอบ
- [ ] พีระมิด: space = `num-row-1`, star = `2*row+1`

**บทที่ 5**
- [ ] `range(start, stop, step)` ไม่รวม stop
- [ ] Loop idioms: largest / count / sum / average / filter / search
- [ ] หา smallest ต้องเริ่มด้วย `None` + `is None`
- [ ] `for` วนกับ string / list / `.split()` ได้
