""" Triangle """

def main():
    """Triangle"""
    side_a = int(input())
    side_b = int(input())
    side_c = int(input())

    if side_a + side_b <= side_c or side_a + side_c <= side_b or side_b + side_c <= side_a:
        print("NOT A TRIANGLE")
        return

    sides = [side_a, side_b, side_c]
    sides.sort()
    shortest = sides[0]
    middle = sides[1]
    longest = sides[2]

    if side_a == side_b and side_b == side_c:
        print("EQUILATERAL")
    elif shortest * shortest + middle * middle == longest * longest:
        print("RIGHT TRIANGLE")
    elif side_a == side_b or side_b == side_c or side_a == side_c:
        print("ISOSCELES")
    else:
        print("SCALENE")

if __name__ == "__main__":
    main()
