""" Ramen Bowl """


def main():
    """Ramen Bowl"""
    n = int(input())
    count = {}
    for _ in range(n):
        x = int(input())
        count[x] = count.get(x, 0) + 1
    print(max(count.values()))


if __name__ == "__main__":
    main()
