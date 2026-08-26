""" FakeThaiPlus """

def main():
    """FakeThaiPlus"""
    name = input().strip()
    age = int(input())
    income = int(input())
    welfare_card = input().strip()
    family_members = int(input())

    if age < 18:
        print(name, "NOT ELIGIBLE")
        return

    if welfare_card == "Y":
        level = "GOLD"
        money = 3000
    elif income <= 15000:
        level = "GOLD"
        money = 3000
    elif income <= 30000:
        level = "SILVER"
        money = 1500
    else:
        print(name, "NOT ELIGIBLE")
        return

    if family_members >= 3:
        money = money + 500

    print(name, level, money)

if __name__ == "__main__":
    main()
