""" เข้าแถว """


def main():
    """เข้าแถว"""
    n = int(input().split()[0])
    h = [int(x) for x in input().split()]
    a = [int(x) for x in input().split()]
    pre = [0] * n
    m = 0
    for i in range(n):
        pre[i] = m
        m = max(m, h[i])
    out = [str(max(0, pre[x - 1] - h[x - 1] + 1)) for x in a]
    print("\n".join(out))


if __name__ == "__main__":
    main()
