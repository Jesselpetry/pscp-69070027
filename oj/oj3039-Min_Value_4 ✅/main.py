""" ค่าน้อยที่สุด (4 ค่า) """

def main():
    """ ค่าน้อยที่สุด (4 ค่า) """
    n = int(input())
    s = []
    for i in range (n):
        s.insert(i, int(input()))
    s.sort(reverse=False)
    top_1 = s[0]
    print(top_1)

if __name__ == "__main__":
    main()
