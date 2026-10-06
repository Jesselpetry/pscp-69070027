""" Count All Vowel """


def main():
    """Count All Vowel"""
    n = int(input())
    v = "AEIOU"
    cnt = 0
    seen = set()
    for _ in range(n):
        ch = input().strip()
        if ch in v:
            cnt += 1
            seen.add(ch)
    print(cnt)
    print("YES" if len(seen) == 5 else "NO")


if __name__ == "__main__":
    main()
