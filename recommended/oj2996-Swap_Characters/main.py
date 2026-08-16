""" [LEARNING LOGS] สลับตัวอักษร """


def main():
    """[LEARNING LOGS] สลับตัวอักษร"""
    text = input()

    # [::-1] คือการตัดข้อความแบบเดินถอยหลัง (step = -1) ได้ข้อความกลับด้าน
    print(text[::-1].lower())


if __name__ == "__main__":
    main()
