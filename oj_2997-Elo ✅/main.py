""" Elo """

def main():
    """Elo"""
    A = int(input())
    B = int(input())
    s = input()
    EA = 1 / (1+10**((B - A)/400))
    EB = 1 / (1+10**((A - B)/400))
    if s == "A":
        print(f"{EA:.2f}")
    else:
        print(f"{EB:.2f}")

if __name__ == "__main__":
    main()
