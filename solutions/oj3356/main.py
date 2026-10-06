""" Bus Seat """


def main():
    """Bus Seat"""
    per_row = int(input())
    rows = int(input())
    mine = int(input())

    blocks = []
    for top in range(per_row - 1, 0, -2):
        block = []
        for p in (top, top - 1):
            cells = []
            for c in range(1, rows + 1):
                seat = (c - 1) * per_row + p + 1
                cells.append("XX" if seat == mine else f"{seat:02d}")
            block.append(" ".join(cells))
        blocks.append("\n".join(block))
    print("\n\n".join(blocks))


if __name__ == "__main__":
    main()
