""" Electric_Using """


def main():
    """Electric_Using"""
    n = int(input())                 # จำนวนหน่วยไฟฟ้าที่ใช้
    tiers = [(10, 5), (40, 7), (50, 10), (100, 12)]   # (จำนวนหน่วยในช่วง, ราคา/หน่วย)
    energy = 0.0
    remaining = n
    for width, rate in tiers:
        used = min(remaining, width)
        energy += used * rate
        remaining -= used
    energy += remaining * 15         # หน่วยที่ 201 เป็นต้นไป หน่วยละ 15 บาท
    vat = energy * 0.07              # VAT 7% คิดจากค่าไฟก่อนรวม FT
    ft = n * 0.5                     # FT อัตราคงที่ 0.50 บาท/หน่วย
    print(f"{energy + vat + ft:.1f}")


if __name__ == "__main__":
    main()
