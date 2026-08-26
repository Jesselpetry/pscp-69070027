""" สงคราม...ส่งด่วน """

def main():
    """สงคราม...ส่งด่วน"""
    origin, destination = input().split()
    weight = float(input())

    if origin == "BKK" and destination == "CNX":
        start_fee = 10
        weight_fee = 30
    elif origin == "CNX" and destination == "UBP":
        start_fee = 15
        weight_fee = 40
    elif origin == "UBP" and destination == "BKK":
        start_fee = 20
        weight_fee = 40
    elif origin == "BKK" and destination == "PKT":
        start_fee = 25
        weight_fee = 50
    elif origin == "PKT" and destination == "CNX":
        start_fee = 30
        weight_fee = 60
    elif origin == "UBP" and destination == "PKT":
        start_fee = 40
        weight_fee = 70
    else:
        print("Error")
        return

    total = start_fee + weight * weight_fee

    print(f"{total:.2f}")

if __name__ == "__main__":
    main()
