""" แคลอรี่ """


def main():
    """แคลอรี่"""
    total = 0
    while True:
        choice = int(input())
        if choice == 5:
            break
        if choice == 1:
            total += 100
        elif choice == 2:
            total += 120
        elif choice == 3:
            total += 200
        elif choice == 4:
            total += 60
    print("Bye Bye")
    print(f"Total Calories: {total}")


if __name__ == "__main__":
    main()
