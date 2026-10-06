""" Day08-0_02-Backward """


def main():
    """Day08-0_02-Backward"""
    data = []
    while True:
        s = input()
        if s == "NULL":
            break
        data.append(s)
    for s in reversed(data):
        print(s)


if __name__ == "__main__":
    main()
