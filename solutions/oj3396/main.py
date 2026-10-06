""" แซงรอบ """


def main():
    """แซงรอบ"""
    n, k = map(int, input().split())
    s = [int(input()) for _ in range(n)]
    mn = min(s)
    ans = 0
    for x in s:
        if k * (x - mn) < x:
            ans += 1
    print(ans)


if __name__ == "__main__":
    main()
