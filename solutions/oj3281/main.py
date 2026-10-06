""" ijudge-itkmitl """

def main():
    """ijudge-itkmitl"""
    link = input()

    prefix = "https://ijudge.it.kmitl.ac.th/problems/"

    rest = ""
    valid = False

    if link.startswith(prefix):
        rest = link[len(prefix):]
        if rest.endswith("/"):
            rest = rest[:-1]
        if len(rest) == 4 and rest.isdigit():
            valid = True

    if valid and rest[0] <= "3":
        print(rest[0], "STAR")
    else:
        print("INVALID")

if __name__ == "__main__":
    main()
