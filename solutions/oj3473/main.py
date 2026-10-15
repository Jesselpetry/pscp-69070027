""" FourDirections """


def main():
    """FourDirections"""
    s = input().strip()
    mid1 = {"U": " ***  ", "D": "  *   ", "L": " *    ", "R": "   *  "}
    mid2 = {"U": "* * * ", "D": "* * * ", "L": "***** ", "R": "***** "}
    mid3 = {"U": "  *   ", "D": " ***  ", "L": " *    ", "R": "   *  "}
    print("".join("  *   " for _ in s))
    print("".join(mid1[c] for c in s))
    print("".join(mid2[c] for c in s))
    print("".join(mid3[c] for c in s))
    print("".join("  *   " for _ in s[:-1]) + "  * ")


if __name__ == "__main__":
    main()
