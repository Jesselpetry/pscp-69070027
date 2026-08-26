""" หาจำนวนเฉพาะ """

def main():
    """หาจำนวนเฉพาะ"""
    start, end = input().split()
    start = int(start)
    end = int(end)

    primes = []
    for number in range(start, end + 1):
        if number < 2:
            continue
        is_prime = True
        for divisor in range(2, int(number ** 0.5) + 1):
            if number % divisor == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(str(number))

    if len(primes) > 0:
        print(" ".join(primes))
    print("Total primes:", len(primes))

if __name__ == "__main__":
    main()
