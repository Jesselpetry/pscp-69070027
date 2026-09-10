""" LastStand """


def main():
    """LastStand"""
    raw = input().strip().strip("[]")          # ตัดวงเล็บของ list ออก
    nums = [int(x) for x in raw.split(",")]
    for x in nums:
        print(abs(x) % 10)                     # หลักสุดท้ายของแต่ละตัว


if __name__ == "__main__":
    main()
