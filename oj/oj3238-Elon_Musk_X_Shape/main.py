""" Elon Musk (X-shape) """

def main():
    """Elon Musk (X-shape)"""
    size, symbol = input().split()
    size = int(size)

    center = (size - 1) / 2

    for row in range(size):
        line = ""
        for column in range(size):
            if column == row or column == size - 1 - row:
                if symbol == "#":
                    line = line + "#"
                else:
                    distance = int(abs(row - center))
                    line = line + chr(ord(symbol) + distance)
            else:
                line = line + "-"
        print(line)

if __name__ == "__main__":
    main()
