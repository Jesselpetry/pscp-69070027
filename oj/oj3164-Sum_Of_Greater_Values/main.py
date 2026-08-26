""" ผลรวมของค่าที่มากกว่า """

import sys

def main():
    """ผลรวมของค่าที่มากกว่า"""
    data = sys.stdin.read().split()
    pairs = int(data[0])

    greater_values = []
    total = 0

    for index in range(pairs):
        first = int(data[1 + index * 2])
        second = int(data[2 + index * 2])
        if first > second:
            greater = first
        else:
            greater = second
        greater_values.append(str(greater))
        total = total + greater

    print(" + ".join(greater_values), "=", total)

if __name__ == "__main__":
    main()
