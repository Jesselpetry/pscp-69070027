""" เดินเล่นในงานเทศกาล """

def main():
    """เดินเล่นในงานเทศกาล"""
    moves = input().strip()

    x = 0
    y = 0

    for move in moves:
        if move == "N":
            y = y + 1
        elif move == "S":
            y = y - 1
        elif move == "E":
            x = x + 1
        elif move == "W":
            x = x - 1

    distance = abs(x) + abs(y)

    print(x, y, distance)

if __name__ == "__main__":
    main()
