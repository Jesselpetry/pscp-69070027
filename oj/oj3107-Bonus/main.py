""" Bonus """

def main():
    """Bonus"""
    position, years, salary = input().split()
    years = int(years)
    salary = int(salary)

    if position == "M":
        bonus = 1500
        if years < 5:
            rate = 6
        elif years < 10:
            rate = 8
        else:
            rate = 10
    elif position == "B":
        bonus = 1000
        if years < 5:
            rate = 5
        elif years < 10:
            rate = 6
        else:
            rate = 7
    else:
        bonus = 500
        if years < 5:
            rate = 4
        elif years < 10:
            rate = 5
        else:
            rate = 6

    total = bonus + salary * rate / 100

    print(int(total))

if __name__ == "__main__":
    main()
