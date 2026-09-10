""" พูดจาภาษากระต่าย """


def main():
    """พูดจาภาษากระต่าย"""
    raw = input().strip()
    s = raw.upper()                       # ตัวพิมพ์เล็ก/ใหญ่ถือว่าเหมือนกัน
    n = len(s)
    for i, ch in enumerate(s):
        if ch == "A":
            if i == 0 or s[i - 1] not in ("R", "A"):   # A ต้องตามหลัง R (หรือ A)
                print("no", i)
                return
        elif ch == "R":
            if i + 1 >= n or s[i + 1] != "A":           # หลัง R ต้องมี A
                print("no", i)
                return
        elif ch == "B":
            if i + 1 >= n or s[i + 1] not in ("I", "T"):   # หลัง B ต้องมี I หรือ T
                print("no", i)
                return
        elif ch not in ("I", "T"):                      # ตัวอักษรนอกภาษากระต่าย
            print("no", i)
            return
    if not any(c in "RAB" for c in s):    # มีแต่ I / T ตัดสินไม่ได้
        print("unknown", n)
        return
    best = run = 0                        # A ที่ยาวติดกันที่สุด
    for ch in s:
        run = run + 1 if ch == "A" else 0
        best = max(best, run)
    print("yes", best)


if __name__ == "__main__":
    main()
