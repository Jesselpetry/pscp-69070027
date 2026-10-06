""" รหัสเซฟ """

def main():
    """ รหัสเซฟ """
    pass_char = "H"
    pass_digit = "4567"
    pass_char_input = str(input(""))
    pass_digit_input = str(input(""))

    if (pass_char_input == pass_char) and (pass_digit_input == pass_digit):
        print("safe unlocked")
    elif (pass_char_input == pass_char) and (pass_digit_input != pass_digit):
        print("safe locked - change digit")
    elif (pass_char_input != pass_char) and (pass_digit_input == pass_digit):
        print("safe locked - change char")
    else:
        print("safe locked")

if __name__ == "__main__":
    main()
