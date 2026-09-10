""" Simple Roman Numerals """

def main():
    """Simple Roman Numerals"""
    n = int(input())

    if n < 0:
        print("Error : Please input positive number")
    elif not n or n > 9:
        print("Error : Out of range")
    else:
        roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
        print(roman[n])

if __name__ == "__main__":
    main()
