""" [LEARNING LOGS] RGB Mixed """


def mix_color(c1, c2):
    """ผสมค่าสีเดียว: เฉลี่ยแบบปัดลง"""
    return (c1 + c2) // 2


def main():
    """[LEARNING LOGS] RGB Mixed"""
    r1, g1, b1 = map(int, input().split())    # RGB ของสีแรก
    r2, g2, b2 = map(int, input().split())    # RGB ของสีที่สอง
    r = mix_color(r1, r2)
    g = mix_color(g1, g2)
    b = mix_color(b1, b2)
    print(r, g, b)


if __name__ == "__main__":
    main()
