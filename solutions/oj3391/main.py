""" สะสมเหรียญเวทย์มนตร์ """


def main():
    """สะสมเหรียญเวทย์มนตร์"""
    n = int(input())
    fire = 0
    water = 0
    earth = 0
    for _ in range(n):
        a = [int(x) for x in input().split()]
        fire += max(a[0], a[3])
        water += max(a[1], a[4])
        earth += max(a[2], a[5])
    print("Total:", fire + water + earth)
    print("Fire:", fire)
    print("Water:", water)
    print("Earth:", earth)
    print("Bonus:", "YES" if fire > water + earth else "NO")


if __name__ == "__main__":
    main()
