""" Meteorite """


def main():
    """Meteorite"""
    a = float(input())
    b = int(input())
    c = float(input())
    ans = 0
    count = 1
    w = a
    while w >= c:
        ans += count
        count *= b
        w /= b
    print(ans)


if __name__ == "__main__":
    main()
