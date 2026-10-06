""" Array ฮาเฮ """


def main():
    """Array ฮาเฮ"""
    a = []
    for i in range(3):
        a.append(int(input()))
        print("Input number", i + 1, "stored.")
    while True:
        c = int(input())
        if c == 0:
            break
        if c == 1:
            print("Original order:", *a)
        elif c == 2:
            print("Descending order:", *sorted(a, reverse=True))
        elif c == 3:
            print("Ascending order:", *sorted(a))


if __name__ == "__main__":
    main()
