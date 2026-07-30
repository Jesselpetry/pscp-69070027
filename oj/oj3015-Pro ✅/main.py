""" Pro """

def main():
    """Pro"""
    x = int(input())
    y = int(input())
    a = int(input())
    z = int(input())

    groups = z // x
    rem = z % x
    paid_count = groups * y + rem
    print(paid_count * a)

if __name__ == "__main__":
    main()
