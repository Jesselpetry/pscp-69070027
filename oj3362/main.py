""" บุพเพสันนิวาส """


def pad_to(name, length):
    """ต่ออักษรตัวหน้าของชื่อตัวเองไปเรื่อย ๆ จนยาวเท่า length"""
    i = 0
    while len(name) < length:
        name += name[i]
        i += 1
    return name


def main():
    """บุพเพสันนิวาส"""
    a = input().rstrip("\n")
    b = input().rstrip("\n")
    length = max(len(a), len(b))
    a, b = pad_to(a, length), pad_to(b, length)
    love = set("love")
    charm = "".join(
        "w" if (a[i].lower() in love or b[i].lower() in love) else "$"
        for i in range(length)
    )
    w_count = charm.count("w")
    best = run = 0                         # w ที่ติดกันยาวสุด
    for ch in charm:
        run = run + 1 if ch == "w" else 0
        best = max(best, run)
    if w_count % 2 == 1:                   # เลขคี่ ไม่เป็นมงคล เติมความยาว run
        charm += str(best)
    elif best < 2:                         # เลขคู่แต่ไม่มี w ติดกัน 2 ตัว
        charm += "#"
    print(charm)


if __name__ == "__main__":
    main()
