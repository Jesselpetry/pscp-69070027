""" PickThemAgain """


def main():
    """PickThemAgain"""
    nums = [int(x) for x in input().split()]
    picked = [x for x in nums if not x % 3 or not x % 5]
    if not picked:
        print("Nope")
        return
    for item in reversed(picked):
        print(item)


if __name__ == "__main__":
    main()
