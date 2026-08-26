""" ไฟคริสตมาส """

def main():
    """ไฟคริสตมาส"""
    first_color, amount = input().split()
    amount = int(amount)

    colors = ["Red", "Green", "Blue"]

    if first_color == "R":
        start = 0
    elif first_color == "G":
        start = 1
    else:
        start = 2

    lights = []
    for position in range(amount):
        lights.append(colors[(start + position) % 3])

    print(" ".join(lights))

if __name__ == "__main__":
    main()
