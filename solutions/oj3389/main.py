""" Smart Trash Collector """


def main():
    """Smart Trash Collector"""
    n = int(input())
    names = ["Plastic", "Can", "Glass"]
    for _ in range(n):
        a = [float(x) for x in input().split()]
        parts = ["{:.1f}".format(sum(a))]
        if sum(a) > 50:
            parts.append("Overloaded")
        for i in range(3):
            if a[i] > 20:
                parts.append("Check Type " + names[i])
        print(", ".join(parts))


if __name__ == "__main__":
    main()
