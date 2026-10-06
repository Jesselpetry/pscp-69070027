""" เกมสะสมแต้ม """

def main():
    """เกมสะสมแต้ม"""
    rounds = int(input())
    score = 0

    for _ in range(rounds):
        command = input().strip()
        if command == "+":
            score += 10
        else:
            score -= 5

    print(score)

if __name__ == "__main__":
    main()
