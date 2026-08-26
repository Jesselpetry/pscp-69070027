""" Stats """

def main():
    """Stats"""
    amount = int(input())

    total = 0
    smallest = 0
    largest = 0

    for index in range(amount):
        number = int(input())
        total = total + number
        if index == 0:
            smallest = number
            largest = number
        elif number < smallest:
            smallest = number
        elif number > largest:
            largest = number

    average = total / amount

    print(f"MIN: {smallest:.3f}")
    print(f"MAX: {largest:.3f}")
    print(f"AVG: {average:.3f}")

if __name__ == "__main__":
    main()
