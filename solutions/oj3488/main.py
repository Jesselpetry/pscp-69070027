""" ไฟส่อง """


def main():
    """ไฟส่อง"""
    n = int(input())
    cov = [False] * 360
    for _ in range(n):
        a, b = map(int, input().split())
        if a < b:
            for k in range(a, b):
                cov[k] = True
        else:
            for k in range(a, 360):
                cov[k] = True
            for k in range(0, b):
                cov[k] = True
    if all(cov):
        print(360)
        return
    ans = 0
    run = 0
    for v in cov + cov:
        if v:
            run += 1
            if run > ans:
                ans = run
        else:
            run = 0
    print(ans)


if __name__ == "__main__":
    main()
