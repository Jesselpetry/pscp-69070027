""" Heads and Legs """


def main():
    """Heads and Legs"""
    animals = int(input())
    legs = int(input())
    # rabbits have 4 legs, birds 2: rabbits + birds = animals and
    # 4*rabbits + 2*birds = legs  ->  rabbits = legs/2 - animals
    if legs % 2 == 0:
        rabbits = legs // 2 - animals
        birds = animals - rabbits
        if rabbits >= 0 and birds >= 0:
            print(f"{rabbits} {birds}")
            return
    print("Impossible")


if __name__ == "__main__":
    main()
