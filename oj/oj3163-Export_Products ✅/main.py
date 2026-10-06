""" สินค้าส่งออก """

def main():
    """สินค้าส่งออก"""
    amount = int(input())

    total = 0
    even_count = 0
    odd_count = 0

    for _ in range(amount):
        stock = int(input())
        total = total + stock
        if not stock % 2:
            even_count = even_count + 1
        else:
            odd_count = odd_count + 1

    print("SUM", total)
    print("EVEN", even_count)
    print("ODD", odd_count)

if __name__ == "__main__":
    main()

