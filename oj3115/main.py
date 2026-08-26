""" Arcade of Time: Store Check """

import sys

def main():
    """Arcade of Time: Store Check"""
    data = sys.stdin.read().split()
    position = 0

    shops = int(data[position])
    position = position + 1
    checks = int(data[position])
    position = position + 1

    opening = [0] * 1442

    for _ in range(shops):
        start = int(data[position])
        position = position + 1
        stop = int(data[position])
        position = position + 1
        opening[start] = opening[start] + 1
        opening[stop] = opening[stop] - 1

    running = 0
    for minute in range(1441):
        running = running + opening[minute]
        opening[minute] = running

    answers = []
    for _ in range(checks):
        moment = int(data[position])
        position = position + 1
        answers.append(str(opening[moment]))

    print(" ".join(answers))

if __name__ == "__main__":
    main()
