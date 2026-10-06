""" กระต่ายน้อยกินราเมน """

def main():
    """กระต่ายน้อยกินราเมน"""
    size, ramen_type = input().split()

    if size == "S":
        if ramen_type == "R":
            price = 60
        else:
            price = 80
    elif size == "M":
        if ramen_type == "R":
            price = 80
        else:
            price = 100
    else:
        if ramen_type == "R":
            price = 100
        else:
            price = 120

    topping = input().split()

    if topping[0] == "P":
        price = price + int(topping[1]) * 15
    elif topping[0] == "E":
        price = price + int(topping[1]) * 10

    print(price)

if __name__ == "__main__":
    main()
