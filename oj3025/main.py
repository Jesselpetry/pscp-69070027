""" Season """

def main():
    """Season"""
    month = int(input())
    day = int(input())

    winter = [1,2]
    spring = [4,5]
    summer = [7,8]
    fall = [10,11]

    if (month in winter) or (month == 12 and day >= 21) or (month == 3 and day < 21):
        print("winter")
    elif (month in spring) or (month == 3 and day >= 21) or (month == 6 and day < 21):
        print("spring")
    elif (month in summer) or (month == 6 and day >= 21) or (month == 9 and day < 21):
        print("summer")
    elif (month in fall) or (month == 9 and day >= 21) or (month == 12 and day < 21):
        print("fall")

if __name__ == "__main__":
    main()
