""" [LEARNING LOGS] แปลงดอกไม้ """


def main():
    """[LEARNING LOGS] แปลงดอกไม้"""
    length, count = map(int, input().split())
    planted = 0
    strip = 0
    while planted < count:
        strip += 1
        cells = length * (2 * length * strip - length + 1) // 2
        planted += cells
    print(strip)


if __name__ == "__main__":
    main()
