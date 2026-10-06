""" ผ่านหรือไม่ ค่าเฉลี่ยรายวิชา """

def main():
    """ผ่านหรือไม่ ค่าเฉลี่ยรายวิชา"""
    subjects = int(input())

    total = 0.0
    all_passed = True

    for _ in range(subjects):
        score = float(input())
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

