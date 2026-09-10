""" [LEARNING LOGS] BigFrame """


def main():
    """[LEARNING LOGS] BigFrame"""
    # รับข้อความ 5 บรรทัด ตัดช่องว่างท้ายบรรทัดทิ้ง
    lines = [input().rstrip() for _ in range(5)]
    width = max(len(s) for s in lines)          # ความกว้างในสุดของกรอบ
    border = "*" * (width + 4)                   # +4 = ดาวซ้าย+ขวา และช่องว่างข้างละ 1
    print(border)
    for s in lines:
        print("* " + s.ljust(width) + " *")     # เติมช่องว่างขวาให้ยาวเท่ากัน
    print(border)


if __name__ == "__main__":
    main()
