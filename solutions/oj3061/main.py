""" ผ่าน/ไม่ผ่าน """

def main():
    """ผ่าน/ไม่ผ่าน"""
    midterm = int(input(""))
    final = int(input(""))
    score = midterm + final
    if score >= 50:
        print(score)
        print("pass")
    else:
        print(score)
        print("fail")

if __name__ == "__main__":
    main()
