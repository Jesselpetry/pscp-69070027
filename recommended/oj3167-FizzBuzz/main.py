""" FizzBuzz """


def main():
    """FizzBuzz"""
    n = int(input())

    for i in range(1, n + 1):
        # ต้องเช็กเงื่อนไขที่เจาะจงที่สุด (หารด้วย 15 ลงตัว) ก่อนเสมอ
        if i % 15 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)


if __name__ == "__main__":
    main()
