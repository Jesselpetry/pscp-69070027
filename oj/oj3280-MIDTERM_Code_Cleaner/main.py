""" CODE CLEANER """

import sys

def main():
    """CODE CLEANER"""
    text = sys.stdin.readline().rstrip("\n")

    letter_count = 0
    digit_count = 0
    code = ""

    for character in text:
        if character.isalpha():
            letter_count = letter_count + 1
            code = code + character.upper()
        elif character.isdigit():
            digit_count = digit_count + 1
            code = code + character
        else:
            if not code.endswith("-"):
                code = code + "-"

    code = code.strip("-")

    if code == "":
        code = "NONE"

    print("CODE =", code)
    print("LETTERS =", letter_count)
    print("DIGITS =", digit_count)

if __name__ == "__main__":
    main()
