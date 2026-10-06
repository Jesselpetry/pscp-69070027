""" Filter """

import ast


def main():
    """Filter"""
    d = ast.literal_eval(input())
    thr = float(input())
    out = []
    for k in sorted(d):
        if d[k] >= thr:
            out.append(k + "\t" + "%.2f" % d[k])
    if out:
        print("\n".join(out))
    else:
        print("Nope")


if __name__ == "__main__":
    main()
