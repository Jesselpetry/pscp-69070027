""" เข้าแถว """


def main():
    """เข้าแถว"""
    n, l = map(int, input().split())
    h = [int(x) for x in input().split()]
    a = [int(x) for x in input().split()]
    pre = [0] * n
    m = 0
    for i in range(n):
        pre[i] = m
        if h[i] > m:
            m = h[i]
    out = []
    for x in a:
        need = pre[x - 1] - h[x - 1] + 1
        if need < 0:
            need = 0
        out.append(str(need))
    print("\n".join(out))


if __name__ == "__main__":
    main()
