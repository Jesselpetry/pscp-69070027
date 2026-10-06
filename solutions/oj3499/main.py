""" Noodle """


def main():
    """Noodle"""
    p = int(input())
    pay = int(input())
    c = pay - p
    if c == 0:
        print("Good!")
    elif c < 0:
        print("Need more cash!")
    else:
        print(c)


if __name__ == "__main__":
    main()
