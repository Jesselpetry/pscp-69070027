""" Tuple's Sad life """


def main():
    """Tuple's Sad life"""
    t = tuple(input().split())
    x = input().strip()
    n = t.count(x)
    idx = t.index(x)
    row = " ".join([str(idx)] * n)
    for _ in range(n):
        print(row)


if __name__ == "__main__":
    main()
