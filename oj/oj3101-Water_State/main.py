""" สถานะน้ำ """

def main():
    """สถานะน้ำ"""
    temperature = int(input())
    unit = input().strip().upper()

    if unit == "F":
        celsius = (temperature - 32) * 5 / 9
    else:
        celsius = temperature

    if celsius <= 0:
        print("solid")
    elif celsius >= 100:
        print("gas")
    else:
        print("liquid")

if __name__ == "__main__":
    main()
