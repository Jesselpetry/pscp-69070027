""" Divide3Or5 """


def main():
    """Divide3Or5"""
    n = int(float(input()))
    print(sum(i for i in range(1, n + 1) if i % 3 == 0 or i % 5 == 0))


if __name__ == "__main__":
    main()
