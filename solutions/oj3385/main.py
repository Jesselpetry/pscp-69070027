""" BusStop I """


def main():
    """BusStop I"""
    p = int(input())
    n = int(input())
    stops = []
    for _ in range(n):
        stops.append(list(map(int, input().split())))
    stops.sort(key=lambda x: x[0])

    bus = []
    ans = 0
    for stop in stops:
        s = stop[0]
        dests = stop[1:]
        ans += bus.count(s)
        bus = [d for d in bus if d != s]
        for d in dests:
            if d <= s or d > n:
                continue
            if len(bus) < p:
                bus.append(d)
            else:
                break
    print(ans)


if __name__ == "__main__":
    main()
