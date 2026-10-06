""" Sairahat """


def main():
    """Sairahat"""
    s = input().strip()
    last = int(s[4:8])
    if s[:2] == "68" and s[2:4] == "07" and 1 <= last <= 328:
        print("Yes")
    else:
        print("No")


if __name__ == "__main__":
    main()
