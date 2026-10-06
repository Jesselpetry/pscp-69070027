""" เหมือนกันหมด """

def main():
    """เหมือนกันหมด"""
    n1 = int(input())
    n2 = int(input())
    n3 = int(input())
    if n1 == n2 and n2 == n3:
        print("all the same")
    elif n1 != n2 and n2 != n3 and n1 != n3:
        print("all different")
    else:
        print("neither")

if __name__ == "__main__":
    main()
