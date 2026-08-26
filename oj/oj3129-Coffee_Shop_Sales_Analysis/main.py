""" วิเคราะห์ยอดขายร้านกาแฟ """

def main():
    """วิเคราะห์ยอดขายร้านกาแฟ"""
    days = int(input())

    total = 0
    highest = 0
    lowest = 0

    for day in range(days):
        sold = int(input())
        total = total + sold
        if day == 0:
            highest = sold
            lowest = sold
        elif sold > highest:
            highest = sold
        elif sold < lowest:
            lowest = sold

    average = total / days

    print(total)
    print(highest)
    print(lowest)
    print(round(average, 1))

if __name__ == "__main__":
    main()
