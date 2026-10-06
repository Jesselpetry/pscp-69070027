""" Cat in the Bag """


def main():
    """Cat in the Bag"""
    lst = []
    while True:
        s = input()
        if s == "-1":
            break
        low = s.lower()
        if "cat" in low:
            lst.append(low)
    print(f"The number of cat in bag {len(lst)}")
    print(f"List of cat {lst}")


if __name__ == "__main__":
    main()
