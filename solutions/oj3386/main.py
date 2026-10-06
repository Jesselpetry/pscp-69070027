""" Duplicate I """


def main():
    """Duplicate I"""
    m = int(input())
    n = int(input())
    a = set()
    for _ in range(m):
        a.add(int(input()))
    b = set()
    for _ in range(n):
        b.add(int(input()))
    ans = sorted(a & b, reverse=True)
    if ans:
        for x in ans:
            print(x)
    else:
        print("Nope")


if __name__ == "__main__":
    main()
