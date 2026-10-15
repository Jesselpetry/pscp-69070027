""" 3nPlus1 """


def main():
    """3nPlus1"""
    while True:
        n = int(input())
        if n == 0:
            break
        length = 1  # count n itself
        while n != 1:
            if n % 2 == 0:
                n //= 2
            else:
                n = 3 * n + 1
            length += 1
        print(length)


if __name__ == "__main__":
    main()
