""" RealThaiPlus """

import sys

def main():
    """RealThaiPlus"""
    data = sys.stdin.read().split()
    position = 0

    wallet = int(data[position])
    position = position + 1
    days = int(data[position])
    position = position + 1

    monthly_left = 1000
    bought_count = 0
    government_total = 0

    for _ in range(days):
        items = int(data[position])
        position = position + 1
        daily_left = 200

        for _ in range(items):
            price = int(data[position])
            position = position + 1

            my_part = int(price * 40 // 100)
            government_help = price - my_part

            if government_help > daily_left:
                government_help = daily_left
            if government_help > monthly_left:
                government_help = monthly_left

            must_pay = price - government_help

            if wallet >= must_pay:
                wallet = wallet - must_pay
                daily_left = daily_left - government_help
                monthly_left = monthly_left - government_help
                government_total = government_total + government_help
                bought_count = bought_count + 1

    print(bought_count)
    print(wallet)
    print(government_total)

if __name__ == "__main__":
    main()
