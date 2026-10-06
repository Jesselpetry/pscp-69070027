""" CaesarV2 """


def main():
    """CaesarV2"""
    lines = []
    while True:
        try:
            lines.append(input())
        except EOFError:
            break
    text = "\n".join(lines)
    words = ["what", "when", "why", "which", "this", "there", "where",
             "the", "is", "am", "are", "you", "we", "they", "he", "she", "it"]
    wset = set(words)
    best = -1
    ans = text
    for s in range(26):
        out = []
        for c in text:
            if "a" <= c <= "z":
                out.append(chr((ord(c) - 97 - s) % 26 + 97))
            elif "A" <= c <= "Z":
                out.append(chr((ord(c) - 65 - s) % 26 + 65))
            else:
                out.append(c)
        dec = "".join(out)
        score = 0
        for t in dec.lower().split():
            clean = "".join(ch for ch in t if "a" <= ch <= "z")
            if clean in wset:
                score += 1
        if score > best:
            best = score
            ans = dec
    print(ans)


if __name__ == "__main__":
    main()
