""" ส่งต่อ """


def main():
    """ส่งต่อ"""
    n, s = map(int, input().split())
    nxt = [0] * (n + 1)
    for i in range(1, n + 1):
        nxt[i] = int(input())
    seen = set()
    cur = s
    while cur != 0 and cur not in seen:
        seen.add(cur)
        cur = nxt[cur]
    print(len(seen))


if __name__ == "__main__":
    main()
