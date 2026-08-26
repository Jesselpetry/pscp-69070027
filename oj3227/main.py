""" ไพ่ 44 ใบ """

def main():
    """ไพ่ 44 ใบ"""
    card = input().strip().upper()

    rank = card[:-1]
    suit = card[-1]

    if rank == "A":
        rank_name = "ace"
    elif rank == "J":
        rank_name = "jack"
    elif rank == "Q":
        rank_name = "queen"
    elif rank == "K":
        rank_name = "king"
    else:
        rank_name = rank

    if suit == "D":
        suit_name = "diamonds"
    elif suit == "H":
        suit_name = "hearts"
    elif suit == "S":
        suit_name = "spades"
    else:
        suit_name = "clubs"

    print(rank_name, "of", suit_name)

if __name__ == "__main__":
    main()
