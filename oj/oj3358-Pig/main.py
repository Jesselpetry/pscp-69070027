""" Pig """


def main():
    """Pig"""
    num_pairs = int(input().strip())
    weights = [int(x) for x in input().split()]
    heavier = [
        max(weights[2 * i], weights[2 * i + 1]) for i in range(num_pairs)
    ]

    if num_pairs == 1:
        print(heavier[0])
        return

    equation = " + ".join(str(w) for w in heavier)
    print(f"{equation} = {sum(heavier)}")


if __name__ == "__main__":
    main()
