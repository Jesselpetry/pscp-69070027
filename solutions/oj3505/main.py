""" PickNum """


def main():
    """PickNum"""
    a = input().split()
    p = 0
    n = 0
    z = 0
    for x in a:
        v = int(x)
        if v > 0:
            p += 1
        elif v < 0:
            n += 1
        else:
            z += 1
    print(f"Positive: {p}")
    print(f"Negative: {n}")
    print(f"Zero: {z}")


if __name__ == "__main__":
    main()
