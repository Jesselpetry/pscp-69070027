""" HorizontalHistogram """


def main():
    """HorizontalHistogram"""
    s = input()
    order = [chr(c) for c in range(97, 123)] + [chr(c) for c in range(65, 91)]
    for ch in order:
        c = s.count(ch)
        if c:
            bar = ""
            for i in range(1, c + 1):
                bar += "-"
                if i % 5 == 0 and i != c:
                    bar += "|"
            print(ch + " : " + bar)


if __name__ == "__main__":
    main()
