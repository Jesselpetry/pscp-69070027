""" ผลรวมกำลัง 2 """

def main():
    """ผลรวมกำลัง 2"""
    limit = int(input())

    total = 0
    for number in range(1, limit + 1):
        total = total + number * number

    print(total)

if __name__ == "__main__":
    main()
