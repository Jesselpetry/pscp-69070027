""" FizzBuzz """


def main():
    """FizzBuzz"""
    n = int(input())

    for i in range(1, n + 1):
        # ต้องเช็กเงื่อนไขที่เจาะจงที่สุด (หารด้วย 15 ลงตัว) ก่อนเสมอ
        if not i % 15:
            print("FizzBuzz")
        elif not i % 3:
            print("Fizz")
        elif not i % 5:
            print("Buzz")
        else:
            print(i)


if __name__ == "__main__":
    main()
