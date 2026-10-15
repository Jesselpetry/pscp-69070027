""" Kangaroo """


def main():
    """Kangaroo"""
    a = int(input())
    b = int(input())
    c = int(input())
    # a jump lands on a free integer strictly between the other two, so each
    # move shrinks a span; jumping over the larger gap first and keeping all
    # remaining room on one side drains it one cell at a time -> max moves is
    # the larger of the two initial gaps
    print(max(b - a - 1, c - b - 1))


if __name__ == "__main__":
    main()
