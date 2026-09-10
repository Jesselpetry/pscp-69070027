""" ขายรถยนต์ """
import sys


def main():
    """ขายรถยนต์"""
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    values = [data[2 + 2 * i] for i in range(n)]   # V_i (ราคา P_i เรียงมากไปน้อยอยู่แล้ว)
    never_sold = 0
    suffix_max = 0                                 # ค่า V ที่ดีที่สุดของรุ่นที่ถูกกว่า
    for v in reversed(values):
        if v <= suffix_max:                       # มีรุ่นถูกกว่าที่ดีกว่าเสมอ
            never_sold += 1
        suffix_max = max(suffix_max, v)
    print(never_sold)


if __name__ == "__main__":
    main()
