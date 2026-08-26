""" ผ่านหรือไม่ ค่าเฉลี่ยรายวิชา """

import sys

def main():
    """ผ่านหรือไม่ ค่าเฉลี่ยรายวิชา"""
    data = sys.stdin.read().split()
    subjects = int(data[0])

    total = 0
    all_passed = True

    for index in range(1, subjects + 1):
        score = int(data[index])
        total = total + score
        if score < 50:
            all_passed = False

    average = total / subjects

    print(f"{average:.1f}")
    if all_passed and average >= 60:
        print("PASS")
    else:
        print("FAIL")

if __name__ == "__main__":
    main()
