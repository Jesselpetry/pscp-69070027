""" List Prime (Sieve of Eratosthenes) """


def main():
    """List Prime (Sieve of Eratosthenes)"""
    n = int(input())
    is_prime = [True] * (n + 1)
    if n >= 0:
        is_prime[0] = False
    if n >= 1:
        is_prime[1] = False
    i = 2
    while i * i <= n:
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
        i += 1
    if n >= 2 and is_prime[n]:
        print("Yes")
        primes = [str(k) for k in range(2, n + 1) if is_prime[k]]
        print(" ".join(primes))
    else:
        print("No")


if __name__ == "__main__":
    main()
