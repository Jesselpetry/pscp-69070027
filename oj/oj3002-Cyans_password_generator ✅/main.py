""" Safe Password """

def main():
    """ Safe Password """
    first_name = input("")
    last_name = input("")
    age = input("")
    password = ""

    if len(first_name) >= 5 and len(last_name) >= 5:
        password = first_name[:2] + last_name[-1] + age[-1]
    else:
        password = first_name[:1] + age + last_name[-1]
    print(password)

if __name__ == "__main__":
    main()
