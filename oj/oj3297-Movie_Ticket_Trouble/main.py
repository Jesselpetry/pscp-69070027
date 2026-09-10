""" ตั๋วหนังสุดป่วน """
import sys


def main():
    """ตั๋วหนังสุดป่วน"""
    data = sys.stdin.read().split()
    seats = int(data[0])                 # จำนวนที่นั่งทั้งหมดในโรง
    out = []
    for i in range(1, len(data) - 1, 2):   # อ่านทีละคู่ (อายุ, จำนวนตั๋ว)
        age = int(data[i])
        want = int(data[i + 1])
        if age < 15:                     # ภาพยนตร์เรท 15+
            out.append("-1")
            continue
        if want > seats:                 # ที่นั่งไม่พอ
            out.append("-2")
            continue
        if 15 <= age <= 22:              # โปรนักเรียน ลด 20%
            price = 150 * 0.8
        elif age >= 60:                  # โปรผู้สูงวัย ลด 50%
            price = 150 * 0.5
        else:
            price = 150
        seats -= want
        total = int(price * want)
        out.append(f"{total} {seats}")
        if seats == 0:
            break
    print("\n".join(out))


if __name__ == "__main__":
    main()
