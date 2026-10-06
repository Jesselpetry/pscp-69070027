""" GCD_v2 """


def main():
    """GCD_v2"""
    a = int(input())
    b = int(input())
    while b:
        a, b = b, a % b
    print(a)


if __name__ == "__main__":
    main()
