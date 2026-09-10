""" Elon Musk (X-shape) """


def main():
    """Elon Musk (X-shape)"""
    raw = input().strip().split()
    size = int(raw[0])
    symbol = raw[1]

    for row in range(size):
        line = []
        for col in range(size):
            if col in (row, size - 1 - row):
                if symbol == "#":
                    line.append("#")
                else:
                    dist = abs(row - size // 2)
                    line.append(chr(ord(symbol) + dist))
            else:
                line.append("-")
        print("".join(line))


if __name__ == "__main__":
    main()
