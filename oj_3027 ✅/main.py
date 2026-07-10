""" กระต่ายน้อยล้อมรั้วลวดหนาม """

def main():
    """กระต่ายน้อยล้อมรั้วลวดหนาม"""
    n = str(input())
    price = int(input())
    nn = n.split(" ")

    width = int(nn[0])
    long = int(nn[1])
    height = int(nn[2])

    print((height * (width + long)) * 2)
    print((height * (width + long)) * 2 * price)


if __name__ == "__main__":
    main()
