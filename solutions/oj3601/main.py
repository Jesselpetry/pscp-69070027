""" มากี่คน """


def main():
    """มากี่คน"""
    male = 0
    female = 0
    while True:
        card = int(input())
        if card < 0:
            break
        if card % 2 == 0:
            female += 1
        else:
            male += 1
    print(f"{male} {female} {male + female}")


if __name__ == "__main__":
    main()
