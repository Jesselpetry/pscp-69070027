""" Triangle """


def main():
    """Triangle"""
    side_a = int(input())
    side_b = int(input())
    side_c = int(input())

    if (side_a + side_b <= side_c) or (side_a + side_c <= side_b) or (side_b + side_c <= side_a):
        print("NOT A TRIANGLE")
        return

    if side_a == side_b == side_c:
        print("EQUILATERAL")
        return

    is_right = False
    if side_a * side_a + side_b * side_b == side_c * side_c:
        is_right = True
    elif side_a * side_a + side_c * side_c == side_b * side_b:
        is_right = True
    elif side_b * side_b + side_c * side_c == side_a * side_a:
        is_right = True

    if is_right:
        print("RIGHT TRIANGLE")
        return

    if side_a == side_b or side_b == side_c or side_a == side_c:
        print("ISOSCELES")
        return

    print("SCALENE")


if __name__ == "__main__":
    main()
