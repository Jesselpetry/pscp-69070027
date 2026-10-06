""" Adventurer's Backpack """


def main():
    """Adventurer's Backpack"""
    line = input()
    new = input()
    if line == "Empty":
        bag = []
    else:
        bag = line.split(",")
    if new == "Stone":
        print("I don't need this!")
        print(bag)
    else:
        if len(bag) >= 5:
            bag.pop(0)
        bag.append(new)
        print(bag)


if __name__ == "__main__":
    main()
