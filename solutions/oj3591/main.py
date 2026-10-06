""" Olympic """


def main():
    """Olympic"""
    n = int(input())
    rows = []
    for _ in range(n):
        p = input().split()
        name = p[0]
        g = int(p[1])
        s = int(p[2])
        b = int(p[3])
        rows.append((name, g, s, b))
    rows.sort(key=lambda r: (-r[1], -r[2], -r[3], r[0]))
    prev = None
    rank = 0
    for i in range(n):
        name, g, s, b = rows[i]
        key = (g, s, b)
        if key != prev:
            rank = i + 1
            prev = key
        print(rank, name, g, s, b, g + s + b)


if __name__ == "__main__":
    main()
