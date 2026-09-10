""" ค่าตั๋ว """

def main():
    """ค่าตั๋ว"""
    age = int(input(""))
    types = input()
    student = ["s","S"]
    if age < 18 or types in student:
        print("20")
    else:
        print("50")

if __name__ == "__main__":
    main()
