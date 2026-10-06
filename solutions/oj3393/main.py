""" นักสำรวจถ้ำ """


def main():
    """นักสำรวจถ้ำ"""
    n = int(input())
    a = input().split()
    pos = a.index("1")
    treasure = a.index("2")
    s = input().strip()
    for c in s:
        if c == "R":
            np = pos + 1
        else:
            np = pos - 1
        if np < 0 or np >= n:
            continue
        pos = np
        if pos == treasure:
            break
    res = ["0"] * n
    res[treasure] = "2"
    res[pos] = "1"
    print(" ".join(res))


if __name__ == "__main__":
    main()
