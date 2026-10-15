""" RuleofThree """


def main():
    """RuleofThree"""
    n = int(input())
    best_price = None
    best_weight = None
    best_ratio = None  # price per gram; the smallest is the best value
    for _ in range(n):
        price = float(input())
        weight = float(input())
        ratio = price / weight
        if (
            best_ratio is None
            or ratio < best_ratio - 1e-9
            or (abs(ratio - best_ratio) <= 1e-9 and price < best_price)
        ):
            best_ratio = ratio
            best_price = price
            best_weight = weight
    print(f"{best_price:.2f} {best_weight:.2f}")


if __name__ == "__main__":
    main()
