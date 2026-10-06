""" Heatwave Stats """


def main():
    """Heatwave Stats"""
    n = int(input())
    nums = [float(x) for x in input().split()]
    nums.sort()
    total = sum(nums)
    avg = total / n
    if n % 2 == 1:
        median = nums[n // 2]
    else:
        median = (nums[n // 2 - 1] + nums[n // 2]) / 2
    alert = 0
    for x in nums:
        if x >= 37.0:
            alert += 1
    print("SUM=%.2f" % total)
    print("AVG=%.2f" % avg)
    print("MEDIAN=%.2f" % median)
    print("MAX=%.2f" % nums[-1])
    print("MIN=%.2f" % nums[0])
    print("ALERT=%d" % alert)
    print("SORTED=" + " ".join("%.2f" % x for x in nums))


if __name__ == "__main__":
    main()
