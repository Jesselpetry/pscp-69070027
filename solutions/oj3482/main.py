""" นักล่าอสูร """

import sys


def main():
    """นักล่าอสูร"""
    order = [
        ("Spider Demon", 1), ("Swamp Demon", 2), ("Arrow Demon", 1),
        ("Hand Demon", 2), ("Drum Demon", 3), ("Mugen Train", 2),
        ("Upper Moon", 3),
    ]
    guesses = iter(int(x) for x in sys.stdin.read().split())
    queue = list(order)
    kills = 0
    attacks = 0
    out = []
    while kills < 5:
        name, weak = queue.pop(0)
        out.append(name)
        wrong = 0
        while True:
            g = next(guesses)
            attacks += 1
            if g == weak:
                out.append("kill")
                kills += 1
                break
            wrong += 1
            if wrong == 2:
                out.append("back")
                queue.append((name, weak))
                break
    out.append(str(attacks))
    print("\n".join(out))


if __name__ == "__main__":
    main()
