""" B - Fully pair? """


def main():
    """B - Fully pair?"""
    s = input()
    res = []
    seen = set()
    for ch in s:
        if ch not in seen:
            seen.add(ch)
            if s.count(ch) % 2 == 1:
                res.append(ch)
    if res:
        print("".join(res))
    else:
        print("fully paired")


if __name__ == "__main__":
    main()
