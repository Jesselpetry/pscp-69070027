""" Paper Cut """


def gaps(cuts, end):
    r = []
    prev = 0
    for x in cuts:
        r.append(x - prev)
        prev = x
    r.append(end - prev)
    return r


def main():
    """Paper Cut"""
    w, h = map(int, input().split())
    input()
    xs = list(map(int, input().split()))
    ys = list(map(int, input().split()))
    a = sorted(gaps(xs, w), reverse=True)
    b = sorted(gaps(ys, h), reverse=True)
    first = a[0] * b[0]
    second = max(a[0] * b[1], a[1] * b[0])
    print(first)
    print(second)


if __name__ == "__main__":
    main()
