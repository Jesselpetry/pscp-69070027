""" Name of Card """


def main():
    """Name of Card"""
    ranks = {"A": "Ace", "J": "Jack", "Q": "Queen", "K": "King"}
    suits = {"D": "Diamonds", "H": "Hearts", "S": "Spades", "C": "Clubs"}
    s = input().strip().upper()
    suit = s[-1]
    rank = s[:-1]
    name = ranks.get(rank, rank)
    print(f"{name} of {suits[suit]}")


if __name__ == "__main__":
    main()
