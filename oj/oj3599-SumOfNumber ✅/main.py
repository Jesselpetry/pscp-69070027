""" SumOfNumber """


def main():
    """SumOfNumber"""
    target = int(input())
    total = 0
    while total != target:
        num = int(input())
        if num == -1:
            break
        total += num
    print(total)


if __name__ == "__main__":
    main()
