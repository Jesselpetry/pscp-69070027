""" คำนวณราคาสินค้าโปรโมชั่น """

def main():
    """คำนวณราคาสินค้าโปรโมชั่น"""
    pencil, notebook, color_box = input().split()
    pencil = int(pencil)
    notebook = int(notebook)
    color_box = int(color_box)

    total = pencil * 25 + notebook * 40 + color_box * 55
    pieces = pencil + notebook + color_box

    if pieces >= 3:
        total = total * 90 / 100

    print(int(total))

if __name__ == "__main__":
    main()
