""" สลากกินแบ่ง """

def main():
    """สลากกินแบ่ง"""
    winning_letter, winning_number = input().split()
    my_letter, my_number = input().split()

    same_letter = my_letter == winning_letter
    last_two = my_number[-2:] == winning_number[-2:]
    last_three = my_number[-3:] == winning_number[-3:]

    if same_letter and my_number == winning_number:
        prize = 1000000
    elif my_number == winning_number:
        prize = 100000
    elif same_letter and last_three:
        prize = 2000
    elif same_letter and last_two:
        prize = 1000
    elif last_three:
        prize = 200
    elif last_two:
        prize = 100
    elif same_letter:
        prize = 20
    else:
        prize = 0

    print(prize)

if __name__ == "__main__":
    main()
