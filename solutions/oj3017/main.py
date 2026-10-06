""" [LEARNING LOGS] Bill """

def main():
    """[LEARNING LOGS] Bill"""
    subtotal = float(input())
    service_charge = subtotal / 10
    if service_charge < 50:
        service_charge = 50
    elif service_charge > 1000:
        service_charge = 1000
    vat = (subtotal + service_charge) * 0.07
    total = subtotal + service_charge + vat
    print(f"{total:.2f}")

if __name__ == "__main__":
    main()
