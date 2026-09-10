""" Right Arrow """


def main():
    """Right Arrow"""
    k = int(input())          # ความกว้าง (จำนวน '*' ต่อบรรทัด)
    n = int(input())          # ความสูง เป็นเลขคี่
    mid = n // 2              # แถวกลางที่เยื้องเข้ามากที่สุด
    for row in range(n):
        indent = mid - abs(row - mid)   # แถวกลางเยื้องมากสุด ปลายบน/ล่างชิดซ้าย
        print(" " * indent + "*" * k)


if __name__ == "__main__":
    main()
