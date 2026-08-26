""" สหกรณ์โรงเรียน """

from decimal import Decimal, ROUND_HALF_UP

def main():
    """สหกรณ์โรงเรียน"""
    member = input().strip().upper()
    items = int(input())

    total = Decimal("0")
    for _ in range(items):
        price = Decimal(input().strip())
        total = total + price

    if member == "Y":
        total = total * Decimal("0.95")
    elif total >= 500:
        total = total * Decimal("0.97")

    result = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    print(result)

if __name__ == "__main__":
    main()
