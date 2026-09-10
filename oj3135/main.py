""" ของขวัญและขโมย """

def main():
    """ของขวัญและขโมย"""
    people, step, thief = input().split()
    people = int(people)
    step = int(step)
    thief = int(thief)

    current = 1
    count = 1

    while current != thief:
        current = (current - 1 + step) % people + 1
        if current == 1:
            break
        count = count + 1

    print(count)

if __name__ == "__main__":
    main()
