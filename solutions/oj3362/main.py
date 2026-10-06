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
    name_a = input().rstrip("\n")
    name_b = input().rstrip("\n")
    length = max(len(name_a), len(name_b))
    name_a = pad_to(name_a, length)
    name_b = pad_to(name_b, length)
    love = set("love")
    charm = "".join(
        "w" if (name_a[i].lower() in love or name_b[i].lower() in love) else "$"
        for i in range(length)
    )
    w_count = charm.count("w")
    best = run = 0
    for ch in charm:
        run = run + 1 if ch == "w" else 0
        best = max(best, run)
    if w_count % 2 == 1:
        charm += str(best)
    elif best < 2:
        charm += "#"
    print(charm)


if __name__ == "__main__":
    main()
