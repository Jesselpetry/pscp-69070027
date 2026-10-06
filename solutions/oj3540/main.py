""" DigitV3 """


def main():
    """DigitV3"""
    ones = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
            "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
            "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
            "nineteen": 19}
    tens = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
            "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}
    total = 0
    cur = 0
    for w in input().split():
        if w in ones:
            cur += ones[w]
        elif w in tens:
            cur += tens[w]
        elif w == "hundred":
            cur *= 100
        elif w == "thousand":
            total += cur * 1000
            cur = 0
    total += cur
    print(total)


if __name__ == "__main__":
    main()
