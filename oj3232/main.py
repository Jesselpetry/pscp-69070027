""" กบน้อยกระโดด """

def main():
    """กบน้อยกระโดด"""
    first_jump, target = input().split()
    first_jump = int(first_jump)
    target = int(target)

    total = 0
    jumps = 0
    distance = first_jump

    while distance > 0 and total < target:
        total = total + distance
        jumps = jumps + 1
        distance = distance - 2

    if total >= target:
        print(jumps)
    else:
        print(-1)

if __name__ == "__main__":
    main()
