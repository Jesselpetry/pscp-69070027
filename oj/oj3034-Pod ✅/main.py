""" Castle """

def main():
    """Castle"""
    n = int(input())

    if n == 1:
        print(0)
        return

    # หาระดับชั้น (r)
    r = int(n ** 0.5)
    if r * r < n:
        r += 1

    # หาว่าห้อง N เป็นห้องลำดับที่ c ของชั้นที่ r
    first_in_row = (r - 1) ** 2 + 1
    c = n - first_in_row + 1

    # ถ้า c เป็นเลขคี่ (สามเหลี่ยมชี้ขึ้น)
    if c % 2 == 1:
        ans = 2 * (r - 1)
    # ถ้า c เป็นเลขคู่ (สามเหลี่ยมชี้ลง)
    else:
        ans = 2 * (r - 1) - 1

    print(ans)

if __name__ == "__main__":
    main()
