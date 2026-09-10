""" Arrow """


def main():
    """Arrow"""
    dirs = input().strip()   # สตริงของ R / L ระบุทิศของลูกธนูแต่ละดอก
    n = int(input())         # ขนาดของลูกธนูแต่ละดอก (n >= 2)
    arrows = []
    for d in dirs:
        lines = []
        for row in range(2 * n - 1):
            depth = min(row, 2 * n - 2 - row)   # 0 ที่หัว/ท้าย, n-1 ที่กลาง
            stars = n - depth
            if d == "R":
                lines.append(" " * (2 * depth) + "*" * stars)
            else:                              # d == "L"
                lines.append(" " * (n - 1 - depth) + "*" * stars)
        arrows.append("\n".join(lines))
    print("\n\n".join(arrows))                 # เว้นบรรทัดว่างคั่นแต่ละดอก


if __name__ == "__main__":
    main()
