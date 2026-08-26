""" ชานมไข่มุก """

def main():
    """ชานมไข่มุก"""
    pearl_type, pearl_gram = input().split()
    pearl_gram = int(pearl_gram)

    tea_type, sweet_level, tea_volume = input().split()
    sweet_level = int(sweet_level)
    tea_volume = int(tea_volume)

    if pearl_type == "H":
        pearl_calorie = 5
    elif pearl_type == "O":
        pearl_calorie = 3
    else:
        pearl_calorie = 2

    if tea_type == "R":
        if sweet_level == 1:
            tea_calorie = 12
        elif sweet_level == 2:
            tea_calorie = 18
        else:
            tea_calorie = 25
    elif tea_type == "T":
        if sweet_level == 1:
            tea_calorie = 15
        elif sweet_level == 2:
            tea_calorie = 20
        else:
            tea_calorie = 30
    else:
        if sweet_level == 1:
            tea_calorie = 10
        elif sweet_level == 2:
            tea_calorie = 15
        else:
            tea_calorie = 20

    total = pearl_calorie * pearl_gram + tea_calorie * tea_volume

    print(total)

if __name__ == "__main__":
    main()
