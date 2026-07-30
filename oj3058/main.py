""" BrickBridge """

def main():
    """BrickBridge"""
    a = int(input())
    b = int(input())
    goal = int(input())

    used_big = min(goal // 5, b)

    needed_small = goal - (used_big * 5)

    if needed_small <= a:
        print(needed_small)
    else:
        print(-1)

if __name__ == "__main__":
    main()
