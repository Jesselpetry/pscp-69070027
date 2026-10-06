""" Dart """


def main():
    """Dart"""
    n = int(input())
    total = 0
    for _ in range(n):
        x, y = map(int, input().split())
        d = x * x + y * y
        if d <= 4:
            total += 5
        elif d <= 16:
            total += 4
        elif d <= 36:
            total += 3
        elif d <= 64:
            total += 2
        elif d <= 100:
            total += 1
    print(total)


if __name__ == "__main__":
    main()
