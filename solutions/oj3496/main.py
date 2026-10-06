""" A+B Upgrade """


def main():
    """A+B Upgrade"""
    a = input().strip()
    b = input().strip()
    print(f"{a}{b} + {b}{a} = {int(a + b) + int(b + a)}")


if __name__ == "__main__":
    main()
