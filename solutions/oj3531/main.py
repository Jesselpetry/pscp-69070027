""" MissingNumber """


def main():
    """MissingNumber"""
    n = int(input())
    seen = set()
    while True:
        x = int(input())
        if x == 0:
            break
        seen.add(x)
    for i in range(1, n + 1):
        if i not in seen:
            print(i)


if __name__ == "__main__":
    main()
