""" สมดุลย์ชีวิต """
import sys


def main():
    """สมดุลย์ชีวิต"""
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    hours = data[1:1 + n]                      # เวลาทำงานแต่ละงาน
    big = sum(1 for h in hours if h > 18)      # งานที่ทำให้นอนหลังเที่ยงคืน
    small = n - big                            # งานที่เสร็จก่อนเที่ยงคืน
    # ทุกงาน big (ยกเว้นตัวสุดท้าย) ต้องตามด้วยงาน small หรือวันพัก
    rest = max(0, (big - 1) - small) if big else 0
    print(n + rest)


if __name__ == "__main__":
    main()
