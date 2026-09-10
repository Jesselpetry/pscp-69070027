""" Temperature """

def main():
    """Temperature"""
    temp = float(input())
    temp_m = str(input())
    convert_to = str(input())
    result = 0

    if temp_m == 'C':
        celsius = temp
    elif temp_m == 'F':
        celsius = (temp - 32) * 5/9
    elif temp_m == 'K':
        celsius = temp - 273.15
    elif temp_m == 'R':
        celsius = (temp - 491.67) * 5/9

    if convert_to == 'C':
        result = celsius
    elif convert_to == 'F':
        result = (celsius * 9/5) + 32
    elif convert_to == 'K':
        result = celsius + 273.15
    elif convert_to == 'R':
        result = (celsius + 273.15) * 9/5

    print(f"{result:.2f}")

if __name__ == "__main__":
    main()
