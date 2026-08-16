""" Elo """


def expected_score(rating, opponent_rating):
    """คืนค่าโอกาสชนะของผู้เล่นที่มีเรตติง rating เมื่อเจอ opponent_rating"""
    return 1 / (1 + 10 ** ((opponent_rating - rating) / 400))


def main():
    """Elo"""
    rating_a = int(input())
    rating_b = int(input())
    player = input()

    if player == "A":
        result = expected_score(rating_a, rating_b)
    else:
        result = expected_score(rating_b, rating_a)

    print(f"{result:.2f}")


if __name__ == "__main__":
    main()
