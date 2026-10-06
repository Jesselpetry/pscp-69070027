""" Easy Histogram No Dict """


def main():
    """Easy Histogram No Dict"""
    s = input()
    for c in "abcdefghijklmnopqrstuvwxyz":
        low = s.count(c)
        if low:
            print(f"{c} = {low}")
        up = s.count(c.upper())
        if up:
            print(f"{c.upper()} = {up}")


if __name__ == "__main__":
    main()
