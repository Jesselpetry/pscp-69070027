""" จำนวนในช่วง [A,B] ที่หารด้วย d เหลือเศษ r """

def main():
    """จำนวนในช่วง [A,B] ที่หารด้วย d เหลือเศษ r"""
    start = int(input())
    end = int(input())
    divisor = int(input())
    remainder = int(input())

    count = 0
    for number in range(start, end + 1):
        if number % divisor == remainder:
            count = count + 1

    print(count)

if __name__ == "__main__":
    main()
