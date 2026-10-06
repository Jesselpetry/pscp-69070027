""" Sorry """


def main():
    """Sorry"""
    lst = []
    while True:
        s = input()
        if s == "End":
            break
        if s == "Sorry":
            if lst:
                lst.pop()
        else:
            lst.append(s)
    print(", ".join(lst))


if __name__ == "__main__":
    main()
