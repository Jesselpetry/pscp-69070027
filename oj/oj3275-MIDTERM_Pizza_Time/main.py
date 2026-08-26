""" PIZZA TIME """

def main():
    """PIZZA TIME"""
    members = int(input())
    pieces_each = int(input())
    pieces_per_tray = int(input())

    needed_pieces = members * pieces_each

    trays = needed_pieces // pieces_per_tray
    if needed_pieces % pieces_per_tray != 0:
        trays = trays + 1

    leftover = trays * pieces_per_tray - needed_pieces

    print(needed_pieces)
    print(trays)
    print(leftover)

if __name__ == "__main__":
    main()
