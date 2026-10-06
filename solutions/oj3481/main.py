""" ลอดสะพาน """


def main():
    """ลอดสะพาน"""
    first = input().split()
    n = int(first[1])
    bridges = []
    for _ in range(n):
        a, b = map(int, input().split())
        bridges.append((a, b))
    ans = 0
    for a, _ in bridges:
        count = 0
        for lo, hi in bridges:
            if lo <= a < hi:
                count += 1
        if count > ans:
            ans = count
    print(ans)


if __name__ == "__main__":
    main()
