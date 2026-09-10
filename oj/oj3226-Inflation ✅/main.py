""" Inflation """


def main():
    """Inflation"""
    price = float(input())
    years = int(input())

    # เก็บเงินเป็น "สตางค์" (จำนวนเต็ม) เพื่อไม่ให้ float ปัดเศษเพี้ยน
    satang = round(price * 100)
    for _ in range(years):
        # ส่วนที่เพิ่มขึ้นแต่ละปี ตัดเศษทิ้งตั้งแต่สตางค์หลักที่ 3
        satang += satang * 381 // 10000

    # แยกบาทกับสตางค์ด้วยจำนวนเต็ม ไม่แปลงกลับเป็น float
    # เพราะถ้า k เยอะ ค่าจะใหญ่เกินกว่าที่ float เก็บได้
    print(f"{satang // 100}.{satang % 100:02d}")


if __name__ == "__main__":
    main()
