""" Factorial """


def main():
    """Factorial"""
    n = int(input())

    # ตัวสะสมแบบคูณต้องเริ่มที่ 1 (ถ้าเริ่มที่ 0 ผลลัพธ์จะเป็น 0 ตลอด)
    result = 1
    for i in range(2, n + 1):
        result *= i

    print(result)


if __name__ == "__main__":
    main()
