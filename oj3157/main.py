""" เกมสะสมแต้ม """

import sys

def main():
    """เกมสะสมแต้ม"""
    data = sys.stdin.read().split()
    rounds = int(data[0])
    score = 0

    for index in range(1, rounds + 1):
        command = data[index]
        if command == "+":
            score = score + 10
        else:
            score = score - 5

    print(score)

if __name__ == "__main__":
    main()
