""" Left Arrow """


def main():
    """Left Arrow"""
    k = int(input())          # ความกว้าง (จำนวน '*' ต่อบรรทัด)
    n = int(input())          # ความสูง เป็นเลขคี่
    mid = n // 2              # แถวกลางที่ยื่นออกไปซ้ายสุด
    for row in range(n):
        indent = abs(row - mid)   # ยิ่งห่างแถวกลาง ยิ่งเยื้องเข้า
        print(" " * indent + "*" * k)


if __name__ == "__main__":
    main()
