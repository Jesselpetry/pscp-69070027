""" Temperature """


def to_celsius(value, unit):
    """แปลงอุณหภูมิจากหน่วย unit มาเป็นเซลเซียส (หน่วยกลาง)"""
    if unit == "F":
        return (value - 32) * 5 / 9
    if unit == "K":
        return value - 273.15
    if unit == "R":
        return (value - 491.67) * 5 / 9
    return value


def from_celsius(celsius, unit):
    """แปลงอุณหภูมิจากเซลเซียส (หน่วยกลาง) ไปเป็นหน่วย unit"""
    if unit == "F":
        return celsius * 9 / 5 + 32
    if unit == "K":
        return celsius + 273.15
    if unit == "R":
        return (celsius + 273.15) * 9 / 5
    return celsius


def main():
    """Temperature"""
    temperature = float(input())
    source_unit = input()
    target_unit = input()

    # แปลง 2 ขั้นผ่านเซลเซียส เขียนสูตรแค่ 6 อัน แทน 12 อัน
    result = from_celsius(to_celsius(temperature, source_unit), target_unit)
    print(f"{result:.2f}")


if __name__ == "__main__":
    main()
