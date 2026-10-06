""" [LEARNING LOGS] Ink """
import math

def main():
    """Ink"""
    s, n = map(int, input().split())

    for _ in range(n):
        x, y = map(int, input().split())

        area = 3.1416 * (x**2 + y**2)
        time_needed = math.ceil(area / s)
        print(time_needed)

if __name__ == "__main__":
    main()
