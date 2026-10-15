""" Ball """


def main():
    """Ball"""
    height = float(input())
    bounces = 0
    # each bounce reaches 3/5 of the previous peak; once a bounce would be
    # under 1 cm (0.01 m) the ball no longer leaves the ground
    while True:
        height = height * 3 / 5
        if height >= 0.01:
            bounces += 1
        else:
            break
    print(bounces)


if __name__ == "__main__":
    main()
