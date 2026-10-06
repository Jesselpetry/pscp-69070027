""" รหัสต้องไม่ซ้ำกัน """


def main():
    """รหัสต้องไม่ซ้ำกัน"""
    n = int(input())
    nums = list(map(int, input().split()))
    ans = [x for x in nums if nums.count(x) == 1]
    ans.sort()
    print(" ".join(str(x) for x in ans))


if __name__ == "__main__":
    main()
