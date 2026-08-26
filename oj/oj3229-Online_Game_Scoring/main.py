""" ระบบคิดคะแนนเกมออนไลน์ """

def main():
    """ระบบคิดคะแนนเกมออนไลน์"""
    base_score = int(input())
    bonus_score = int(input())
    days_played = int(input())

    total = base_score + bonus_score
    if days_played > 3:
        total = total * 1.5
    total = int(total)

    if total >= 1500:
        rank = 5
    elif total >= 1000:
        rank = 4
    elif total >= 500:
        rank = 3
    elif total >= 200:
        rank = 2
    else:
        rank = 1

    if rank == 5 and days_played >= 7:
        special = 99
    elif rank == 4 and bonus_score > 300:
        special = 88
    else:
        special = 0

    print(total)
    print(rank)
    print(special)

if __name__ == "__main__":
    main()
