""" Conan """

def main():
    """Conan"""
    message = input().strip()
    shift = int(input())

    result = ""
    for letter in message:
        if "a" <= letter <= "z":
            position = ord(letter) - ord("a")
            position = (position + shift) % 26
            result = result + chr(ord("a") + position)
        else:
            result = result + letter

    print(result)

if __name__ == "__main__":
    main()
