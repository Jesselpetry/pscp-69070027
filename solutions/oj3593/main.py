""" FibonacciRecursionV2 """


def fib(n):
    if n == 0:
        return (0, 1)
    a, b = fib(n // 2)
    c = a * (2 * b - a)
    d = a * a + b * b
    if n % 2 == 0:
        return (c, d)
    return (d, c + d)


def main():
    """FibonacciRecursionV2"""
    n = int(input())
    print(fib(n)[0])


if __name__ == "__main__":
    main()
