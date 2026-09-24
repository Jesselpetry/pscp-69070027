""" Teaching schedule """


def main():
    """Teaching schedule"""
    n = int(input())
    a = int(input())
    total = n * a
    if not total:
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
