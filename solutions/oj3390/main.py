""" Array 2D ตรวจสอบ """


def main():
    """Array 2D ตรวจสอบ"""
    g = [[int(x) for x in input().split()] for _ in range(5)]
    r = -1
    c = -1
    for i in range(5):
        if sum(g[i]) % 2 != 0:
            r = i
    for j in range(5):
        if sum(g[i][j] for i in range(5)) % 2 != 0:
            c = j
    print(r, c)


if __name__ == "__main__":
    main()
