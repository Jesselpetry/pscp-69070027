""" ตารางสูตรคูณ """

def main():
    """ตารางสูตรคูณ"""
    number = int(input())

    for multiplier in range(1, 13):
        print(f"{number} * {multiplier} = {number * multiplier}")

if __name__ == "__main__":
    main()
