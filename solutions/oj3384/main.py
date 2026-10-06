""" PickThem """

import ast


def main():
    """PickThem"""
    nums = ast.literal_eval(input())
    ans = [x for x in nums if x % 2 == 0]
    if ans:
        for x in ans:
            print(x)
    else:
        print("Nope")


if __name__ == "__main__":
    main()
