""" สลับหมายเลข """

def main():
    """สลับหมายเลข"""
    n = int(input())
    nn = str(n)[::-1]
    if 10 <= n <= 99:
        o = str(input(""))
        if o == "+":
            print(f"{int(n)} {o} {int(nn)} = {int(n) + int(nn)}")
        elif o == "*":
            print(f"{int(n)} {o} {int(nn)} = {int(n) * int(nn)}")

if __name__ == "__main__":
    main()
