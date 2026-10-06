""" หาร 10 """

def main():
    """หาร 10"""
    n = int(input())
    ans = []
    num = n - (n % 10)

    if not num % 10:
        rounds = num // 10
        for _ in range(rounds+1):
            ans.append(num)
            num = num-10
    print(*ans)

if __name__ == "__main__":
    main()
