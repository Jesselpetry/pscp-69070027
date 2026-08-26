""" พิมพ์สัญลักษณ์ """

def main():
    """พิมพ์สัญลักษณ์"""
    amount = int(input())

    result = ""
    for position in range(1, amount + 1):
        if not position % 5:
            result = result + "X"
        else:
            result = result + "*"

    print(result)

if __name__ == "__main__":
    main()
