""" PM WATCH """

import sys

def main():
    """PM WATCH"""
    data = sys.stdin.read().split()
    days = int(data[0])

    over_count = 0
    peak = 0
    best_streak = 0
    best_start = 0
    current_streak = 0
    current_start = 0

    for day in range(1, days + 1):
        dust = int(data[day])

        if day == 1 or dust > peak:
            peak = dust

        if dust > 50:
            over_count = over_count + 1
            if current_streak == 0:
                current_start = day
            current_streak = current_streak + 1
            if current_streak >= best_streak:
                best_streak = current_streak
                best_start = current_start
        else:
            current_streak = 0

    print("OVER =", over_count)
    print("PEAK =", peak)
    print("STREAK =", best_streak)
    print("START =", best_start)

if __name__ == "__main__":
    main()
