""" PickThemAgain """


def main():
    """PickThemAgain"""
    nums = list(map(int, input().split()))
    picked = [x for x in nums if x % 3 == 0 or x % 5 == 0]
    if not picked:
        print("Nope")
        return
    for x in reversed(picked):                 # จากหลังมาหน้า
        print(x)


if __name__ == "__main__":
    main()
