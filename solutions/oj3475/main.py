""" Muddled Menu """


def main():
    """Muddled Menu"""
    menu = []
    while True:
        line = input()
        if line == "DONE":
            break
        if line == "CLOSED":
            menu = []
            break
        if line == "SOMETHING'S WRONG":
            menu = []
            continue
        if line.startswith("Can't do: "):
            name = line[len("Can't do: "):]
            if name in menu:
                menu.remove(name)
            continue
        name, num = line.rsplit(" #", 1)
        if num == "N":
            menu.append(name)
        else:
            menu.insert(int(num) - 1, name)
    print(f"Full Course: {menu} Reversed: {menu[::-1]}")


if __name__ == "__main__":
    main()
