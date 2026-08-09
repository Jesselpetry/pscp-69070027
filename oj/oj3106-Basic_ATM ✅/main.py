""" Basic ATM """

def main():
    """Basic ATM"""
    n = float(input())

    if 100 <= n <= 20000:
        thoundsands = n // 1000
        n = n-thoundsands * 1000
        five_hundred = n // 500
        n = n-five_hundred * 500
        one_hundred = n // 100
        n = n-one_hundred * 100

        if n > 0:
            print("ERROR")
        else:
            if thoundsands > 0:
                print(f"1000 = {thoundsands:.0f}")
            if five_hundred > 0:
                print(f"500 = {five_hundred:.0f}")
            if one_hundred > 0:
                print(f"100 = {one_hundred:.0f}")

    else:
        print("ERROR")

if __name__ == "__main__":
    main()
