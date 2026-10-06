""" ติดตั้งหลอดไฟ """


def main():
    """ติดตั้งหลอดไฟ"""
    n = int(input())
    h = [int(input()) for _ in range(n)]
    h.sort()
    total = 0
    prefix = 0
    for x in h:
        prefix += x
        total += prefix
    print(total * 2)


if __name__ == "__main__":
    main()
