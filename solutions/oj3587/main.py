""" OneTwo """


def main():
    """OneTwo"""
    n = int(input())
    a = "1"
    b = "2"
    if n == 1:
        print(a)
        return
    if n == 2:
        print(b)
        return
    for _ in range(n - 2):
        a, b = b, b + a
    print(b)


if __name__ == "__main__":
    main()
