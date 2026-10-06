""" Squid Game 3 - Tug-of-War """


def main():
    """Squid Game 3 - Tug-of-War"""
    a = sum(int(input()) for _ in range(10))
    b = sum(int(input()) for _ in range(10))
    if a < b:
        print("A")
    elif b < a:
        print("B")
    else:
        print("AB")


if __name__ == "__main__":
    main()
