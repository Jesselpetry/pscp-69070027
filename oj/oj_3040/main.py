""" แลกเปลี่ยนเงิน """

def main():
    """แลกเปลี่ยนเงิน"""
    coin = int(input(""))
    thb_10 = coin // 10
    coin %= 10
    thb_5 = coin // 5
    coin %= 5
    thb_2 = coin // 2
    coin %= 2
    thb_1 = coin // 1

    print(f"10: {thb_10}")
    print(f"5: {thb_5}")
    print(f"2: {thb_2}")
    print(f"1: {thb_1}")

if __name__ == "__main__":
    main()
