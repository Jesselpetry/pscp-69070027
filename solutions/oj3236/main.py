""" รหัสแฝดเทค """


def main():
    """รหัสแฝดเทค"""
    length = int(input())
    first_code = input().strip()
    second_code = input().strip()

    mismatch = 0
    for position in range(length):
        if int(first_code[position]) + int(second_code[position]) != 9:
            mismatch += 1

    if not mismatch:
        print("YES")
    else:
        print("NO", mismatch)


if __name__ == "__main__":
    main()
