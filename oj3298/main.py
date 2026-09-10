""" กระต่ายน้อยรัก BUU """


def main():
    """กระต่ายน้อยรัก BUU"""
    text = input().strip()
    upper = text.upper()                 # BUU ไม่สนตัวพิมพ์เล็ก/ใหญ่
    if "BUU" in upper:
        best = 0
        for i, ch in enumerate(upper):
            if ch == "B" and upper[i + 1:i + 3] == "UU":
                run = 0                   # นับ U ที่ต่อท้าย B ตัวนี้แบบไม่มีตัวอื่นคั่น
                for c in upper[i + 1:]:
                    if c == "U":
                        run += 1
                    else:
                        break
                best = max(best, run)
        print("Yes", best)
    elif "B" in upper:
        idx = upper.index("B")            # ตำแหน่ง B ตัวแรก
        print(text[:idx + 1] + "U" * (len(text) - idx - 1))
    else:
        pattern = ("BUU" * (len(text) // 3 + 1))[:len(text)]
        print(pattern)


if __name__ == "__main__":
    main()
