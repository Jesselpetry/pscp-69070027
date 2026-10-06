""" Longer """

import math


def main():
    """Longer"""
    r = float(input())
    a = float(input())
    b = float(input())
    c = 2 * math.pi * r
    rect = 2 * (a + b)
    if c > rect:
        print("Circle is longer")
    elif rect > c:
        print("Rectangle is longer")
    else:
        print("Equal")
    print(f"{abs(c - rect):.5f}")


if __name__ == "__main__":
    main()
