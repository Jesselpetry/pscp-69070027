""" BrickBridge """

def main():
    """BrickBridge"""
    a = int(input(""))
    b = int(input(""))
    goal = int(input(""))
    big_brick = b * 5
    all_brick = big_brick + a
    remainder = 0
    if all_brick >= goal:
        remainder = goal % 5
        if remainder <= a:
            print(remainder)
    else:
        print(-1)

if __name__ == "__main__":
    main()
