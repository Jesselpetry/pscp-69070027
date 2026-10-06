""" RectangleArea """

def main():
    """RectangleArea"""
    x1, y1, w1, h1 = map(int, input().split())
    x2, y2, w2, h2 = map(int, input().split())

    xa2, ya2 = x1 + w1, y1 + h1
    xb2, yb2 = x2 + w2, y2 + h2

    overlap_w = min(xa2, xb2) - max(x1, x2)
    overlap_h = min(ya2, yb2) - max(y1, y2)

    if overlap_w > 0 and overlap_h > 0:
        print(overlap_w * overlap_h)
    else:
        print("no overlapping")

if __name__ == "__main__":
    main()
