""" คำนวณค่าแท็กซี่เบื้องต้น """

def main():
    """คำนวณค่าแท็กซี่เบื้องต้น"""
    distance = int(input())

    fare = 35
    if distance > 1:
        if distance <= 10:
            fare = fare + (distance - 1) * 5
        else:
            fare = fare + 9 * 5 + (distance - 10) * 8

    print(fare)

if __name__ == "__main__":
    main()
