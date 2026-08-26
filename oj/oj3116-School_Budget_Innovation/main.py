""" นวัตกรรมงบประมาณโรงเรียน """

def main():
    """นวัตกรรมงบประมาณโรงเรียน"""
    school_name = input().strip()

    upper_name = school_name.upper()
    first_code = ord(upper_name[0])
    last_code = ord(upper_name[-1])
    name_length = len(school_name)

    digits = []
    for place in range(1, 11):
        place_value = place - 1
        if place % 2:
            value = first_code + place_value
        else:
            value = last_code - place_value

        value = value % name_length
        if value > 9:
            value = value % 10

        digits.append(str(value))

    password = digits[2:8]

    print(" ".join(password))

if __name__ == "__main__":
    main()
