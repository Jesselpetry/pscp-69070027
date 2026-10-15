""" [LEARNING LOGS] Shorten """


def main():
    """[LEARNING LOGS] Shorten"""
    nums = []
    while True:
        try:
            line = input().strip()
        except EOFError:
            break
        if not line:
            continue
        v = int(line)
        if v == -1:
            break
        nums.append(v)
    parts = []
    start = prev = nums[0]
    for v in nums[1:]:
        if v == prev + 1:                 # ต่อเนื่องจากตัวก่อนหน้า
            prev = v
            continue
        parts.append(str(start) if start == prev else f"{start}-{prev}")
        start = prev = v
    parts.append(str(start) if start == prev else f"{start}-{prev}")
    print(", ".join(parts))


if __name__ == "__main__":
    main()
