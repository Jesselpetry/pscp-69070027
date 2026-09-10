""" กองชาม """
import sys
from collections import Counter


def main():
    """กองชาม"""
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    sizes = data[1:1 + n]
    # จัดกองได้อิสระ ชามขนาดเท่ากันซ้อนกันไม่ได้
    # จำนวนกองน้อยสุด = จำนวนชามที่มีขนาดซ้ำมากที่สุด
    print(max(Counter(sizes).values()))


if __name__ == "__main__":
    main()
