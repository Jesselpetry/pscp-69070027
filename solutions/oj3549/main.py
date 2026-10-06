""" Book shelf """


def main():
    """Book shelf"""
    books = input().split()
    name = input()
    if name in books:
        books.remove(name)
        print(" ".join(books))
    else:
        print("There are no book with that name on this shelf")


if __name__ == "__main__":
    main()
