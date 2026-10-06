""" Calculator V2 """


def main():
    """Calculator V2"""
    n = int(input())
    length = len(str(n))
    d = 0
    for size in range(1, length + 1):
        low = 10 ** (size - 1)
        high = 10 ** size - 1
        if size == length:
            high = n
        d += (high - low + 1) * size
    total = d + (n - 1)
    if n >= 2:
        total += 1
    print(total)


if __name__ == "__main__":
    main()
