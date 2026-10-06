""" นับเลขคู่และเลขคี่ """

def main():
    """นับเลขคู่และเลขคี่"""
    n1 = float(input())
    n2 = float(input())
    n3 = float(input())

    even = 0
    odd = 0

    if not n1 % 2:
        even += 1
    else:
        odd += 1
    if not n2 % 2:
        even += 1
    else:
        odd += 1
    if not n3 % 2:
        even += 1
    else:
        odd += 1

    print(even)
    print(odd)

if __name__ == "__main__":
    main()
