""" Pad Thai """


def main():
    """Pad Thai"""
    allowed = {
        "Pad Thai Sauce", "Tofu", "Pickle Turnip", "Shrimp",
        "Bean Sprouts", "Noodle", "Chives", "Lime", "Egg", "Oil", "Peanuts",
    }
    used = []
    while True:
        x = input()
        if x == "Cook":
            break
        used.append(x)
    tastes = []
    while True:
        x = input()
        if x == "End":
            break
        tastes.append(x)
    if any(x not in allowed for x in used):
        print("This is not Pad Thai!!!")
    elif set(used) != allowed:
        print("This is bad!")
    elif set(tastes) == {"Sweet", "Sour", "Salty"}:
        print("Delicious!")
    else:
        print("Not Bad...")


if __name__ == "__main__":
    main()
