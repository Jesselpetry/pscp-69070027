""" Nearer """


def main():
    """Nearer"""
    a = int(input())
    b = int(input())
    t = int(input())
    da = abs(a - t)
    db = abs(b - t)
    if da < db:
        print(f"Alice {da}")
    elif db < da:
        print(f"Bob {db}")
    else:
        print(f"Sundaes {da}")


if __name__ == "__main__":
    main()
