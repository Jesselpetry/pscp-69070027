""" ขายรถยนต์ """


def main():
    """ขายรถยนต์"""
    line = input().strip()
    if not line:
        return
    num_cars = int(line)
    values = []
    for _ in range(num_cars):
        row = input().split()
        values.append(int(row[1]))

    never_sold = 0
    suffix_max = 0
    for val in reversed(values):
        if val <= suffix_max:
            never_sold += 1
        else:
            suffix_max = val

    print(never_sold)


if __name__ == "__main__":
    main()
