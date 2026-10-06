""" Calendar """


def main():
    """Calendar"""
    d = int(input())
    m = int(input())
    y = int(input())
    g = y * 360 + m * 30 + d
    dl = 2569 * 360 + 10 * 30 + 2
    print(max(0, dl - g))


if __name__ == "__main__":
    main()
