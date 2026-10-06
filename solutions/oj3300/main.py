""" สมดุลย์ชีวิต """


def main():
    """สมดุลย์ชีวิต"""
    n = int(input())
    big = 0
    count = 0
    while count < n:
        for val in input().split():
            if int(val) > 18:
                big += 1
            count += 1
            if count == n:
                break
    small = n - big
    rest = max(0, (big - 1) - small) if big else 0
    print(n + rest)


if __name__ == "__main__":
    main()
