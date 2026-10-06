""" FibonacciRecursionV1 """


def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def main():
    """FibonacciRecursionV1"""
    n = int(input())
    print(fib(n))


if __name__ == "__main__":
    main()
