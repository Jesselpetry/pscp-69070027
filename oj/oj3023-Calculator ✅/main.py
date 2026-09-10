""" Calculator """

def main():
    """Calculator"""
    n = int(input(""))
    amount = 0
    for i in range(1, n + 1):
        amount += len(str(i)) + 1
    if n == 1:
        print(1)
    else:
        print(amount)

if __name__ == "__main__":
    main()
