""" ตั๋วหนังสุดป่วน """


def main():
    """ตั๋วหนังสุดป่วน"""
    seats = int(input())
    while seats > 0:
        try:
            line = input().strip()
        except EOFError:
            break
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        age = int(parts[0])
        want = int(parts[1])
        if age < 15:
            print("-1")
            continue
        if want > seats:
            print("-2")
            continue
        if 15 <= age <= 22:
            price = 150 * 0.8
        elif age >= 60:
            price = 150 * 0.5
        else:
            price = 150
        seats -= want
        total = int(price * want)
        print(f"{total} {seats}")


if __name__ == "__main__":
    main()
