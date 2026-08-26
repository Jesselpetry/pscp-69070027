""" Suvarnabhumi Airport Parking """

def main():
    """Suvarnabhumi Airport Parking"""
    enter_hour, enter_minute = input().strip().split(".")
    exit_hour, exit_minute = input().strip().split(".")

    enter_total = int(enter_hour) * 60 + int(enter_minute)
    exit_total = int(exit_hour) * 60 + int(exit_minute)

    stay_minutes = exit_total - enter_total
    if stay_minutes < 0:
        stay_minutes = stay_minutes + 24 * 60

    hours = stay_minutes // 60
    if stay_minutes % 60 != 0:
        hours = hours + 1

    if stay_minutes <= 15:
        print("FREE")
    elif hours == 1:
        print(25)
    elif hours == 2:
        print(50)
    elif hours == 3:
        print(80)
    elif hours == 4:
        print(110)
    elif hours == 5:
        print(145)
    elif hours == 6:
        print(180)
    elif hours <= 24:
        print(250)
    else:
        print("ERROR")

if __name__ == "__main__":
    main()
