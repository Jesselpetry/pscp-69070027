""" ผลรวมของค่าที่มากกว่า """

def main():
    """ผลรวมของค่าที่มากกว่า"""
    pairs = int(input())

    greater_values = []
    total = 0

    for _ in range(pairs):
        first = int(input())
        second = int(input())
        if first > second:
            greater = first
        else:
            greater = second
        greater_values.append(str(greater))
        total = total + greater

    if pairs == 1:
        print(greater_values[0])
    elif pairs > 1:
        print(" + ".join(greater_values), "=", total)

if __name__ == "__main__":
    main()

