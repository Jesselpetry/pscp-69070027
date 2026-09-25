""" พอด """


def main():
    """พอด"""
    first_line = input().split()
    if len(first_line) >= 2:
        n, k = int(first_line[0]), int(first_line[1])
    else:
        n = int(first_line[0])
        k = int(input().strip())

    counts = [0] * (k + 1)
    for _ in range(n):
        line = input().strip()
        while not line:
            line = input().strip()
        counts[int(line)] += 1

    min_passengers = min(counts[1:k + 1])
    remaining = n - (min_passengers * k)
    print(remaining)


if __name__ == "__main__":
    main()
