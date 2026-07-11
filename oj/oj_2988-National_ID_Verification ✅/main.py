""" การตรวจสอบบัตรประชาชน """

def main():
    """การตรวจสอบบัตรประชาชน"""
    national_id = input()

    if len(national_id) == 13:
        print("yes")
    else:
        print("no")

if __name__ == "__main__":
    main()
