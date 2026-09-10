""" ไข้หวัดกระต่ายสายพันธุ์ใหม่ """
import sys


def main():
    """ไข้หวัดกระต่ายสายพันธุ์ใหม่"""
    data = sys.stdin.read().split()
    it = iter(data)
    rows, cols = int(next(it)), int(next(it))
    my_r, my_c = int(next(it)), int(next(it))
    n = int(next(it))
    infected = [(int(next(it)), int(next(it))) for _ in range(n)]

    def risk(r, c):
        best = 0
        for ir, ic in infected:
            d = max(abs(r - ir), abs(c - ic))    # ระยะแบบเชบีเชฟ (สี่เหลี่ยมจัตุรัส)
            if d == 0:
                return 100
            if d == 1:
                best = max(best, 60)
            elif d == 2:
                best = max(best, 20)
        return best

    safe = sum(1 for r in range(rows) for c in range(cols) if risk(r, c) == 0)
    print(safe)
    print(f"{risk(my_r, my_c)}%")


if __name__ == "__main__":
    main()
