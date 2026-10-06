""" 113 """


def main():
    """113"""
    s = input().strip()
    st = []
    for c in s:
        st.append(c)
        if len(st) >= 3 and st[-3] == "1" and st[-2] == "1" and st[-1] == "3":
            del st[-3:]
    print("".join(st))


if __name__ == "__main__":
    main()
