""" Hamming """


def main():
    """Hamming"""
    a = input()
    b = input()
    print(sum(1 for x, y in zip(a, b) if x != y))


if __name__ == "__main__":
    main()
