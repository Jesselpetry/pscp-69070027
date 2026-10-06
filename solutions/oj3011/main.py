""" [LEARNING LOGS] Colors """

def main():
    """[LEARNING LOGS] Colors"""
    col_1 = str(input())
    col_2 = str(input())
    allowed_color = ["Red","Blue","Yellow"]
    if (col_1 in allowed_color) and (col_2 in allowed_color):
        if (col_1 == "Red" and col_2 == "Yellow") or (col_1 == "Yellow" and col_2 == "Red"):
            print("Orange")
        elif (col_1 == "Red" and col_2 == "Blue") or (col_1 == "Blue" and col_2 == "Red"):
            print("Violet")
        elif (col_1 == "Yellow" and col_2 == "Blue") or (col_1 == "Blue" and col_2 == "Yellow"):
            print("Green")
        elif col_1 == col_2:
            print(col_1)
    else:
        print("Error")

if __name__ == "__main__":
    main()
