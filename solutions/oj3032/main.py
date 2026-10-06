""" คะแนนสอบ """

def main():
    """คะแนนสอบ"""
    n = int(input())
    s = []
    for i in range (n):
        s.insert(i, int(input()))
    s.sort(reverse=True)
    top_1 = s[0]
    count = 0
    for i in range (n):
        if s[i] == top_1:
            count += 1

    print(top_1)
    print(count)

if __name__ == "__main__":
    main()
