""" Teaching schedule """


def main():
    """Teaching schedule"""
    n = int(input())              # จำนวนคาบสอนใน 1 สัปดาห์
    a = int(input())              # เวลาต่อคาบ (นาที)
    total = n * a                 # เวลาสอนรวม (นาที)
    if total == 0:
        print("No teaching")
        return
    hours, minutes = divmod(total, 60)
    parts = []
    if hours:
        parts.append(f"{hours} hours")
    if minutes:
        parts.append(f"{minutes} minute")
    print(" ".join(parts))


if __name__ == "__main__":
    main()
