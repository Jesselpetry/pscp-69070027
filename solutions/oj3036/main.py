""" [LEARNING LOGS] ปราสาท """


def main():
    """[LEARNING LOGS] ปราสาท"""
    n = int(input())
    if n == 1:
        print(0)
        return
    r = int((n - 1) ** 0.5) + 1
    k = n - 1 - (r - 1) ** 2
    if k % 2 == 1:
        print(2 * r - 3)
    else:
        print(2 * r - 2)


if __name__ == "__main__":
    main()
