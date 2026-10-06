""" GG-EZ """


def main():
    """GG-EZ"""
    g = input().strip()
    d = int(input())
    if (g == "Rov" and d >= 2) or (g == "Valorant" and d >= 7):
        print("GGEZ")
    else:
        print("GGWP")


if __name__ == "__main__":
    main()
