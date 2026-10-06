""" ชานมไข่มุก """

PEARL_CAL = {"H": 5, "O": 3, "J": 2}
TEA_CAL = {
    "R": {1: 12, 2: 18, 3: 25},
    "T": {1: 15, 2: 20, 3: 30},
    "M": {1: 10, 2: 15, 3: 20},
}


def main():
    """ชานมไข่มุก"""
    pearl_type, pearl_gram_str = input().split()
    pearl_gram = float(pearl_gram_str)

    tea_type, sweet_level_str, tea_volume_str = input().split()
    sweet_level = int(sweet_level_str)
    tea_volume = float(tea_volume_str)

    p_cal = PEARL_CAL[pearl_type]
    t_cal = TEA_CAL[tea_type][sweet_level]

    total = p_cal * pearl_gram + t_cal * tea_volume
    if total.is_integer():
        print(int(total))
    else:
        print(total)


if __name__ == "__main__":
    main()
