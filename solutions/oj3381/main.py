""" Point Sorting """


def main():
    """Point Sorting"""
    t = int(input())
    for _ in range(t):
        n = int(input())
        pts = []
        for _ in range(n):
            x, y = map(int, input().split())
            pts.append((x, y))
        pts.sort(key=lambda p: (p[0] + p[1], -p[1]))
        for x, y in pts:
            print(x, y)


if __name__ == "__main__":
    main()
