""" Impostor """

import ast


def main():
    """Impostor"""
    people = {}
    while True:
        line = input().strip()
        if line == "Start":
            break
        d = ast.literal_eval(line)
        for k in d:
            people[k] = d[k]
    dead = set()
    while True:
        line = input().strip()
        if line == "End":
            break
        dead.add(line)
    remain = 0
    for k in people:
        if k not in dead and people[k] == "Impostor":
            remain += 1
    print(str(remain) + " Impostor Remains")
    print("***Alive***")
    for k in sorted(people):
        if k not in dead:
            print(k + " : " + people[k])
    print("***Dead***")
    for k in sorted(people):
        if k in dead:
            print(k + " : " + people[k])


if __name__ == "__main__":
    main()
