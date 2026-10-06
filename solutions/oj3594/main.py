""" 1132-Median """


def main():
    """1132-Median"""
    nums = [float(x) for x in input().split(",")]
    nums.sort()
    n = len(nums)
    if n % 2 == 1:
        ans = nums[n // 2]
    else:
        ans = (nums[n // 2 - 1] + nums[n // 2]) / 2
    print("%.2f" % ans)


if __name__ == "__main__":
    main()
