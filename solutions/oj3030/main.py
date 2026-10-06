""" I will be Saitama! """
import math

def main():
    """I will be Saitama!"""

    target_pushups = int(input())
    target_situps = int(input())
    target_squats = int(input())
    target_run = int(input())

    per_day_pushups = int(input())
    per_day_situps = int(input())
    per_day_run = int(input())
    per_day_squats = int(input())

    days_pushups = math.ceil(target_pushups / per_day_pushups)
    days_situps = math.ceil(target_situps / per_day_situps)
    days_squats = math.ceil(target_squats / per_day_squats)
    days_run = math.ceil(target_run / per_day_run)

    ans = max(days_pushups, days_situps, days_squats, days_run)
    print(ans)

if __name__ == "__main__":
    main()
