""" ตำบลกระสุนตก """


def main():
    """ตำบลกระสุนตก"""
    n = int(input())
    shots = []
    for _ in range(n):
        x, y, d = map(int, input().split())
        shots.append((x, y, d))
    for tx in range(1001):
        for ty in range(1001):
            ok = True
            for x, y, d in shots:
                if (x - tx) ** 2 + (y - ty) ** 2 != d * d:
                    ok = False
                    break
            if ok:
                print(f"{tx} {ty}")
                return


if __name__ == "__main__":
    main()
