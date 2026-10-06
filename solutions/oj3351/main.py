""" พูดจาภาษากระต่าย """


def get_char_error(text, i, ch, length):
    """Check if character at i causes error."""
    err = None
    if ch not in ("R", "A", "B", "I", "T"):
        err = i
    elif ch == "A" and (not i or text[i - 1] not in ("R", "A")):
        err = i
    elif ch == "R":
        err = i if i + 1 >= length else (i + 1 if text[i + 1] != "A" else None)
    elif ch == "B":
        is_bad = text[i + 1] not in ("I", "T") if i + 1 < length else False
        err = i if i + 1 >= length else (i + 1 if is_bad else None)
    return err


def find_error(text):
    """Find first error index in rabbit word."""
    length = len(text)
    for i, ch in enumerate(text):
        err = get_char_error(text, i, ch, length)
        if err is not None:
            return err
    return None


def main():
    """พูดจาภาษากระต่าย"""
    text = input().strip().upper()
    err_pos = find_error(text)
    if err_pos is not None:
        print("no", err_pos)
        return

    if not any(c in "RAB" for c in text):
        print("unknown", len(text))
        return

    best = run = 0
    for ch in text:
        run = run + 1 if ch == "A" else 0
        best = max(best, run)
    print("yes", best)


if __name__ == "__main__":
    main()
