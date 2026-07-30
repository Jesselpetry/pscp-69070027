""" A-E-I-O-U """

def main():
    """A-E-I-O-U"""
    text = str(input().lower())
    vowels = ['a', 'e', 'i', 'o', 'u']
    a = 0
    e = 0
    i = 0
    o = 0
    u = 0
    for char in text:
        if char in vowels:
            if char == 'a':
                a = a + 1
            elif char == 'e':
                e = e + 1
            elif char == 'i':
                i = i + 1
            elif char == 'o':
                o = o + 1
            elif char == 'u':
                u = u + 1
    if a > 0:
        print(f"a : {a}")
    if e > 0:
        print(f"e : {e}")
    if i > 0:
        print(f"i : {i}")
    if o > 0:
        print(f"o : {o}")
    if u > 0:
        print(f"u : {u}")

if __name__ == "__main__":
    main()
