""" การนับสระ """

def main():
    """การนับสระ"""
    text = input().strip()
    vowels = ["a", "e", "i", "o", "u"]

    count = 0
    for letter in text:
        if letter in vowels:
            count = count + 1

    print(count)

if __name__ == "__main__":
    main()
