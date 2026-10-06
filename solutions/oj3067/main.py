""" การเพิ่ม/ลด """

def main():
    """การเพิ่ม/ลด"""
    n1 = float(input())
    n2 = float(input())
    n3 = float(input())
    if n1 < n2 < n3:
        print("increasing")
    elif n1 > n2 > n3:
        print("decreasing")
    else:
        print("neither")

if __name__ == "__main__":
    main()
