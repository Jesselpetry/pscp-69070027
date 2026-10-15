""" ProgressiveTax_Midterm2014 """


def main():
    """ProgressiveTax_Midterm2014"""
    income = int(input())
    # (upper bound of the slab, marginal rate in whole percent)
    brackets = [
        (150000, 0),
        (300000, 5),
        (500000, 10),
        (750000, 15),
        (1000000, 20),
        (2000000, 25),
        (4000000, 30),
    ]
    scaled = 0  # tax * 100, kept integer so there is no float rounding
    lower = 0
    for upper, rate in brackets:
        if income > upper:
            scaled += (upper - lower) * rate
            lower = upper
        else:
            scaled += (income - lower) * rate
            break
    else:
        scaled += (income - lower) * 35
    # the revenue department keeps no satang -> drop the fraction
    print(scaled // 100)


if __name__ == "__main__":
    main()
