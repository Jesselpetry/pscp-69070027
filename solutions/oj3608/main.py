""" Turnstile """


def main():
    """Turnstile"""
    locked = True
    passed = 0
    while True:
        action = input().strip()
        if action == "END":
            break
        if action == "C":
            locked = False
        elif action == "P":
            if not locked:
                passed += 1
                locked = True
    print(passed)


if __name__ == "__main__":
    main()
