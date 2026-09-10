""" [LEARNING LOGS] แปลงดอกไม้ """


def main():
    """[LEARNING LOGS] แปลงดอกไม้"""
    L, N = map(int, input().split())     # L = ความหนาของแถบ, N = จำนวนช่องที่ปลูก
    planted = 0
    strip = 0
    # แถบที่ k กินแนวทแยงที่ L(k-1)+1 ถึง Lk แนวทแยงที่ d มี d ช่อง
    while planted < N:
        strip += 1
        cells = L * (2 * L * strip - L + 1) // 2   # ผลรวมช่องในแถบนี้
        planted += cells
    print(strip)


if __name__ == "__main__":
    main()
