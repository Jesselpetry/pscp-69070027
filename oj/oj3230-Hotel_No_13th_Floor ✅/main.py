""" โรงแรมกลางกรุง ไม่มีชั้น 13 """


def get_floor(digits):
    """Determine floor number."""
    for idx, d in enumerate(digits):
        if d > 5:
            return 14 if idx == 4 else 9 + idx
    return 13


def get_room_first(secret, digits):
    """Determine first room digit."""
    d1, d2, _, d4, d5 = digits
    if secret == secret[::-1]:
        if d1 + d5 > 5:
            return 1
        if d2 * d4 > 5:
            return 2
        return 0

    if d5 and d1 // d5 > 5:
        return 1
    if d2 - d5 > 5:
        return 2
    return 0


def get_room_second(digits):
    """Determine second room digit."""
    if sum(digits) > 25:
        return 1
    digit_prod = 1
    for d in digits:
        digit_prod *= d
    if digit_prod > 55:
        return 2
    return 0


def main():
    """โรงแรมกลางกรุง ไม่มีชั้น 13"""
    secret = input().strip()
    digits = [int(c) for c in secret]

    floor = get_floor(digits)
    room_first = get_room_first(secret, digits)
    room_second = get_room_second(digits)

    print(f"{floor}{room_first}{room_second}")


if __name__ == "__main__":
    main()
