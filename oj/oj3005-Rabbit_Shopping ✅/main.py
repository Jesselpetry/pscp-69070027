""" กระต่ายน้อยจ่ายตลาด """

def main():
    """กระต่ายน้อยจ่ายตลาด"""
    n = str(input())
    nn = n.split(" ")

    carrot = int(nn[0]) * 10
    cabbage = int(nn[1]) * 25
    tomato = int(nn[2]) * 3

    print(carrot + cabbage + tomato)

if __name__ == "__main__":
    main()
