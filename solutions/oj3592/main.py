""" Align """


def main():
    """Align"""
    size = int(input())
    mode = input()
    text = input()
    pad = size - len(text)
    if mode == "left":
        print(text + " " * pad)
    elif mode == "right":
        print(" " * pad + text)
    else:
        left = (pad + 1) // 2
        right = pad - left
        print(" " * left + text + " " * right)


if __name__ == "__main__":
    main()
