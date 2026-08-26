""" ภาษีรถยนต์ """

def main():
    """ภาษีรถยนต์"""
    year = int(input())
    engine_size = int(input())

    if year <= 1990:
        if engine_size <= 1500:
            tax = 1250
        elif engine_size <= 2000:
            tax = 1400
        else:
            tax = 2000
    elif year <= 1999:
        if engine_size <= 1500:
            tax = 1100
        elif engine_size <= 2000:
            tax = 1300
        else:
            tax = 1700
    else:
        if engine_size <= 1500:
            tax = 1000
        elif engine_size <= 2000:
            tax = 1200
        else:
            tax = 1500

    print(tax)

if __name__ == "__main__":
    main()
