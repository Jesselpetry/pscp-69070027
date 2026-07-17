""" Coke """

def main():
    """Coke"""
    promo_useable = 0
    promo_amount = 0

    a = int(input())
    b = int(input())
    c = int(input())
    d = int(input())
    if not d:
        print(0)
        return
    if not b:
        promo_useable = 0
    else:
        promo_useable = (d-1) // b
        promo_amount = promo_useable * c
    normal_price = d - promo_useable
    normal_amount = normal_price * a
    print(promo_amount + normal_amount)

if __name__ == "__main__":
    main()
