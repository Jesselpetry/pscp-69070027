""" Item checker """


def main():
    """Item checker"""
    items = input().split()
    q = input().strip()
    low = [x.lower() for x in items]
    if q.lower() in low:
        print(f"{q} is in the list")
    else:
        print(f"{q} is not in the list")


if __name__ == "__main__":
    main()
