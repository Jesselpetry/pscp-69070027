""" FourDirections """


def main():
    """FourDirections"""
    arrows = {
        "U": ["  *  ", " *** ", "* * *", "  *  ", "  *  "],
        "D": ["  *  ", "  *  ", "* * *", " *** ", "  *  "],
        "L": ["  *  ", " *   ", "*****", " *   ", "  *  "],
        "R": ["  *  ", "   * ", "*****", "   * ", "  *  "],
    }
    s = input().strip()
    for r in range(5):
        print(" ".join(arrows[c][r] for c in s))


if __name__ == "__main__":
    main()
