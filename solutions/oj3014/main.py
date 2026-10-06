""" Milk """

def main():
    """Milk"""
    a = float(input())
    b = float(input())
    c = float(input())
    d = float(input())

    caps = int(d // a)
    total_bottles = caps

    if caps >= b > 0:
        while caps >= b:
            exchanged_bottles = int((caps // b) * c)
            caps = int((caps % b) + exchanged_bottles)
            total_bottles += exchanged_bottles

    print(total_bottles)

if __name__ == "__main__":
    main()
