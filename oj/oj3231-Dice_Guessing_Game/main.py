""" เกมทายลูกเต๋า """

def main():
    """เกมทายลูกเต๋า"""
    guess = int(input())
    result = int(input())

    if guess < 1 or guess > 6 or result < 1 or result > 6:
        print("Invalid")
    elif guess == result:
        print("Correct!")
    else:
        print("Wrong!")

if __name__ == "__main__":
    main()
