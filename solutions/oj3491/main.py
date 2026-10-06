""" RunGame """


def main():
    """RunGame"""
    a = input().split()
    pos = 0
    total = 0
    for x in a:
        v = int(x)
        total += abs(v - pos)
        pos = v
    print(total)


if __name__ == "__main__":
    main()
