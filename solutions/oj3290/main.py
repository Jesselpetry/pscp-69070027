""" Left Arrow """


def main():
    """Left Arrow"""
    k = int(input())
    n = int(input())
    mid = n // 2
    for row in range(n):
        indent = abs(row - mid)
        print(" " * indent + "*" * k)


if __name__ == "__main__":
    main()
