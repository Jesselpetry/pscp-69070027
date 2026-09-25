""" กองชาม """
from collections import Counter


def main():
    """กองชาม"""
    num_bowls = int(input().strip())
    sizes = [int(input().strip()) for _ in range(num_bowls)]
    print(max(Counter(sizes).values()))


if __name__ == "__main__":
    main()
