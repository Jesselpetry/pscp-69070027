""" ปีอธิกสุรทิน """

def main():
    """ปีอธิกสุรทิน"""
    year = int(input())

    if year < 1582:
        if not year % 4:
            print("yes")
        else:
            print("no")

    else:
        if not year % 400:
            print("yes")
        elif not year % 100:
            print("no")
        elif not year % 4:
            print("yes")
        else:
            print("no")

if __name__ == "__main__":
    main()
