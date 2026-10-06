""" GCD_N """

import math


def main():
    """GCD_N"""
    n = int(input())
    ans = int(input())
    for _ in range(n - 1):
        ans = math.gcd(ans, int(input()))
    print(ans)


if __name__ == "__main__":
    main()
