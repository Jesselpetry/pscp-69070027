""" Kabata """


def check(s):
    i = 0
    n = len(s)
    while i < n:
        if s[i:i + 5] == "bakka":
            i += 5
        elif s[i:i + 2] == "ta" or s[i:i + 2] == "ka":
            i += 2
        elif s[i:i + 2] == "ba":
            if s[i + 2:i + 4] == "ka":
                return False
            i += 2
        else:
            return False
    return True


def main():
    """Kabata"""
    n = int(input())
    for _ in range(n):
        s = input()
        if check(s):
            print("yes")
        else:
            print("no")


if __name__ == "__main__":
    main()
