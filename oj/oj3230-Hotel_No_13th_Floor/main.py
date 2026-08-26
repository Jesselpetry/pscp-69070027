""" โรงแรมกลางกรุง ไม่มีชั้น 13 """

def main():
    """โรงแรมกลางกรุง ไม่มีชั้น 13"""
    secret = input().strip()

    digit1 = int(secret[0])
    digit2 = int(secret[1])
    digit3 = int(secret[2])
    digit4 = int(secret[3])
    digit5 = int(secret[4])

    if digit1 > 5:
        floor = 9
    elif digit2 > 5:
        floor = 10
    elif digit3 > 5:
        floor = 11
    elif digit4 > 5:
        floor = 12
    elif digit5 > 5:
        floor = 14
    else:
        floor = 13

    is_palindrome = secret == secret[::-1]

    if is_palindrome:
        if digit1 + digit5 > 5:
            room_first = 1
        elif digit2 * digit4 > 5:
            room_first = 2
        else:
            room_first = 0
    else:
        if digit5 != 0 and digit1 // digit5 > 5:
            room_first = 1
        elif digit2 - digit5 > 5:
            room_first = 2
        else:
            room_first = 0

    digit_sum = digit1 + digit2 + digit3 + digit4 + digit5
    digit_product = digit1 * digit2 * digit3 * digit4 * digit5

    if digit_sum > 25:
        room_second = 1
    elif digit_product > 55:
        room_second = 2
    else:
        room_second = 0

    print(f"{floor}{room_first}{room_second}")

if __name__ == "__main__":
    main()
