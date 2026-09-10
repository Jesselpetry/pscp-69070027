""" Heron of Alexandria """
import math

def main():
    """Heron of Alexandria"""
    a = float(input())
    b = float(input())
    c = float(input())
    s = (a + b + c) / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    print(f"{area:.3f}")

if __name__ == "__main__":
    main()
