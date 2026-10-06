""" isPrime_large """


def main():
    """isPrime_large"""
    n = int(input())
    if n < 2:
        print("NO")
        return
    i = 2
    prime = True
    while i * i <= n:
        if n % i == 0:
            prime = False
            break
        i += 1
    print("YES" if prime else "NO")


if __name__ == "__main__":
    main()
