""" รูปดาว * """


def main():
    """รูปดาว *"""
    n = int(input())
    for count in (n, n - 2, n - 4):
        print("*" * max(count, 0))


if __name__ == "__main__":
    main()
