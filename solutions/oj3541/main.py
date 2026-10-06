""" Coke V2 """


def main():
    """Coke V2"""
    a = int(input())
    b = int(input())
    c = int(input())
    d = int(input())
    if d == 0:
        print(0)
    elif b == 0:
        print(d * a)
    else:
        x = (d - 1) // b
        print((d - x) * a + x * c)


if __name__ == "__main__":
    main()
