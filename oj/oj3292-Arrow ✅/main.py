""" Arrow """


def main():
    """Arrow"""
    dirs = input().strip()
    n = int(input())
    arrows = []
    for d in dirs:
        lines = []
        for row in range(2 * n - 1):
            depth = min(row, 2 * n - 2 - row)
            stars = n - depth
            if d == "R":
                lines.append(" " * (2 * depth) + "*" * stars)
            else:
                lines.append(" " * (n - 1 - depth) + "*" * stars)
        arrows.append("\n".join(lines))
    print("\n\n".join(arrows))


if __name__ == "__main__":
    main()
