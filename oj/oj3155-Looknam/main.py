""" ลูกน้ำ """

def main():
    """ลูกน้ำ"""
    number = input().strip()

    result = ""
    for position in range(len(number)):
        digits_left = len(number) - position
        if position > 0 and not digits_left % 3:
            result = result + ","
        result = result + number[position]

    print(result)

if __name__ == "__main__":
    main()
