""" สินค้าส่งออก """

import sys

def main():
    """สินค้าส่งออก"""
    data = sys.stdin.read().split()
    amount = int(data[0])

    total = 0
    even_count = 0
    odd_count = 0

    for index in range(1, amount + 1):
        stock = int(data[index])
        total = total + stock
        if stock % 2 == 0:
            even_count = even_count + 1
        else:
            odd_count = odd_count + 1

    print("SUM", total)
    print("EVEN", even_count)
    print("ODD", odd_count)

if __name__ == "__main__":
    main()
