""" Factorial """

def main():
    """Factorial"""
    number = int(input())
    result = 1
    for multiplier in range(1, number + 1):
        result = result * multiplier
    print(result)

if __name__ == "__main__":
    main()
