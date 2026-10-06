""" จำนวนสระ """

def main():
    """จำนวนสระ"""
    amount = int(input())
    vowels = ["A", "E", "I", "O", "U"]

    count = 0
    for _ in range(amount):
        letter = input().strip().upper()
        if letter in vowels:
            count = count + 1

    print(count)

if __name__ == "__main__":
    main()
