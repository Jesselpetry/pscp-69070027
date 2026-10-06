""" Hint """
import operator

OPS = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
}


def get_matching_digits(sym, target_str):
    """Return list of digits (0-9) matching the condition."""
    check_fn = OPS[sym]
    target = int(target_str)
    return [d for d in range(10) if check_fn(d, target)]


def main():
    """Hint"""
    sym_u, dig_u = input().split()
    sym_t, dig_t = input().split()
    sym_h, dig_h = input().split()

    units = get_matching_digits(sym_u, dig_u)
    tens = get_matching_digits(sym_t, dig_t)
    hundreds = get_matching_digits(sym_h, dig_h)

    for h in hundreds:
        for t in tens:
            for u in units:
                print(f"{h}{t}{u}")


if __name__ == "__main__":
    main()
