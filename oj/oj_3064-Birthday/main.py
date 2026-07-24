""" วันเกิด """
from datetime import date

def main():
    """วันเกิด"""
    y1 = int(input(""))
    m1 = int(input(""))
    d1 = int(input(""))
    y2 = int(input(""))
    m2 = int(input(""))
    d2 = int(input(""))

    date1 = date(y1, m1, d1)
    date2 = date(y2, m2, d2)

    diff = abs((date1 - date2).days)

    if diff <= 7:
        print("0")
    elif date1 < date2:
        print("1")
    else:
        print("2")

if __name__ == "__main__":
    main()
