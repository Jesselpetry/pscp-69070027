""" BusStop I """


def main():
    """BusStop I"""
    p = int(input())
    n = int(input())
    bus = []
    ans = 0
    for _ in range(n):
        nums = list(map(int, input().split()))
        s = nums[0]
        dests = nums[1:]
        ans += bus.count(s)
        bus = [d for d in bus if d != s]
        for d in dests:
            if d <= s:
                continue
            if len(bus) < p:
                bus.append(d)
            else:
                break
    print(ans)


if __name__ == "__main__":
    main()
