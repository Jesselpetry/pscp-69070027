""" ผลการสอบ """

def main():
    """ผลการสอบ"""
    exercise = int(input(""))
    midterm = int(input(""))
    final = int(input(""))

    if exercise >= 5 and midterm >= 20 and final >= 25:
        print("pass")
    else:
        print("fail")

if __name__ == "__main__":
    main()
