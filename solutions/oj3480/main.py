""" นก """


def main():
    """นก"""
    n = int(input())
    h = list(map(int, input().split()))
    ans = 0
    for i in range(n):
        if i > 0 and h[i - 1] > h[i]:
            continue
        if i < n - 1 and h[i + 1] > h[i]:
            continue
        ans += 1
    print(ans)


if __name__ == "__main__":
    main()
