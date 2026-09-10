""" ค่าน้อยที่สุด """

def main():
    """ค่าน้อยที่สุด"""
    n = []
    for i in range(3):
        n.insert(i, int(input()))
    n.sort(reverse=False)
    print(n[0])

if __name__ == "__main__":
    main()
