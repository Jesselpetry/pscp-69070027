""" กระดาษห่อของขวัญ """

def main():
    """กระดาษห่อของขวัญ"""
    r, h, overlap = map(float, input().split())
    width = h + (2 * r)
    length = (2 * 3.14 * r) + overlap
    print(f"{width:.2f} {length:.2f}")
if __name__ == "__main__":
    main()
