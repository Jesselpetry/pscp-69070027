""" จำนวนสระ """

import sys

def main():
    """จำนวนสระ"""
    data = sys.stdin.read().split()
    amount = int(data[0])
    vowels = ["A", "E", "I", "O", "U"]

    count = 0
    for index in range(1, amount + 1):
        letter = data[index].upper()
        if letter in vowels:
            count = count + 1

    print(count)

if __name__ == "__main__":
    main()
