""" Electric_Using """
from decimal import Decimal, ROUND_HALF_UP


def main():
    """Electric_Using"""
    n = int(input())
    tiers = [(10, 5), (40, 7), (50, 10), (100, 12)]
    energy = Decimal(0)
    rem = Decimal(n)
    for width, rate in tiers:
        used = min(rem, Decimal(width))
        energy += used * Decimal(rate)
        rem -= used
    energy += rem * Decimal(15)
    vat = energy * Decimal("0.07")
    ft_cost = Decimal(n) * Decimal("0.5")
    total = (energy + vat + ft_cost).quantize(
        Decimal("0.1"), rounding=ROUND_HALF_UP
    )
    print(total)


if __name__ == "__main__":
    main()
