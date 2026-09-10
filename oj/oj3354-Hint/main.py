""" Hint """
import operator


def main():
    """Hint"""
    ops = {"==": operator.eq, "!=": operator.ne, ">": operator.gt,
           "<": operator.lt, ">=": operator.ge, "<=": operator.le}
    checks = []
    for _ in range(3):                     # หลักหน่วย, หลักสิบ, หลักร้อย ตามลำดับ
        sym, digit = input().split()
        checks.append((ops[sym], int(digit)))
    for n in range(100, 1000):
        units, tens, hundreds = n % 10, n // 10 % 10, n // 100
        if all(fn(d, ref) for (fn, ref), d in
               zip(checks, (units, tens, hundreds))):
            print(n)


if __name__ == "__main__":
    main()
