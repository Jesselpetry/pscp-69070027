""" ใส่กล่อง """


def main():
    """ใส่กล่อง"""
    w, l, m, n = map(int, input().split())
    box = w * l
    best = box
    for a in range(m, n + 1):
        # เฟส 1: เรียงตามแนวยาว L ทีละแถว จนครบ W แถว
        phase1 = (l // a) * w * a
        # เฟส 2: หมุนของ แล้วเรียงในพื้นที่ที่เหลือท้ายกล่อง กว้าง L%a ยาว W
        phase2 = (w // a) * (l % a) * a
        waste = box - phase1 - phase2
        best = min(best, waste)
    print(best)


if __name__ == "__main__":
    main()
