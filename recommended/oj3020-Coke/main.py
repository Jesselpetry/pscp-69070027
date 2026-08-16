""" Coke """


def main():
    """Coke"""
    normal_price = int(input())
    caps_needed = int(input())
    promo_price = int(input())
    bottles_wanted = int(input())

    if caps_needed == 0:
        # b = 0 คือแลกฝาไม่ได้ ต้องซื้อราคาปกติทุกขวด
        promo_bottles = 0
    else:
        # ขวดแรกต้องซื้อราคาปกติเสมอ จึงคิดจาก (d - 1) และหารแบบปัดลง
        promo_bottles = max(bottles_wanted - 1, 0) // caps_needed

    normal_bottles = bottles_wanted - promo_bottles
    print(promo_bottles * promo_price + normal_bottles * normal_price)


if __name__ == "__main__":
    main()
