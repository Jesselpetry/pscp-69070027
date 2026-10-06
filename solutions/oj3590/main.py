""" Flatten """

import ast


def flat(x):
    r = []
    for e in x:
        if isinstance(e, list):
            r += flat(e)
        else:
            r.append(e)
    return r


def main():
    """Flatten"""
    s = ast.literal_eval(input())
    ans = sorted(flat(s), reverse=True)
    print(ans)


if __name__ == "__main__":
    main()
