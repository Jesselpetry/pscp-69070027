""" ค่าสูงสุด """

def main():
    """ค่าสูงสุด"""
    n = []
    for i in range(3):
        n.insert(i, int(input()))
    n.sort(reverse=True)
    print(n[0])

if __name__ == "__main__":
    main()
