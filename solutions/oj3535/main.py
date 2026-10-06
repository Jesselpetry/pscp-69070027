""" Classify """


def main():
    """Classify"""
    data = {}
    while True:
        s = input().strip()
        if s == "END":
            break
        y = s[0:2]
        f = int(s[2:4])
        data.setdefault(y, {})
        data[y][f] = data[y].get(f, 0) + 1
    for y in sorted(data):
        first = True
        for f in sorted(data[y]):
            label = y if first else "--"
            print(label + " " + str(f) + " " + str(data[y][f]))
            first = False


if __name__ == "__main__":
    main()
