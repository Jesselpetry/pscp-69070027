""" Safe Password """

CORRECT_CHAR = "H"
CORRECT_DIGIT = "4567"


def main():
    """Safe Password"""
    char = input()
    digit = input()

    char_ok = char == CORRECT_CHAR
    digit_ok = digit == CORRECT_DIGIT

    if char_ok and digit_ok:
        print("safe unlocked")
    elif char_ok:
        print("safe locked - change digit")
    elif digit_ok:
        print("safe locked - change char")
    else:
        print("safe locked")


if __name__ == "__main__":
    main()
