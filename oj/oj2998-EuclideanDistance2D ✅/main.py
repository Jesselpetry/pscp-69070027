""" EuclideanDistance2D """
import math as m

def main():
    """EuclideanDistance2D"""
    q1 = float(input())
    q2 = float(input())
    p1 = float(input())
    p2 = float(input())

    solution = m.sqrt((q1 - p1) ** 2 + (q2 - p2) ** 2)

    print(f"{solution}")

if __name__ == "__main__":
    main()
