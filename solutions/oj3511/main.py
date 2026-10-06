""" Rain """


def main():
    """Rain"""
    c = input().strip()
    w = input().strip()
    if c == "Gloomy" and (w == "High" or w == "Medium"):
        print("100%")
    elif c == "Cloudy":
        print("50%")
    elif c == "Clear" and w == "Low":
        print("0%")
    else:
        print("Not sure.")


if __name__ == "__main__":
    main()
