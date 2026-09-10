""" Pig """
import sys


def main():
    """Pig"""
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    weights = data[1:1 + 2 * n]
    heavier = [max(weights[2 * i], weights[2 * i + 1]) for i in range(n)]
    if n == 1:
        print(heavier[0])                 # คู่เดียว แสดงผลลัพธ์ได้เลย
        return
    print(" + ".join(map(str, heavier)) + f" = {sum(heavier)}")


if __name__ == "__main__":
    main()
