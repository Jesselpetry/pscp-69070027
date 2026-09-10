""" OverlapCircle """

def main():
    """OverlapCircle"""
    x1 = int(input())
    y1 = int(input())
    r1 = int(input())
    x2 = int(input())
    y2 = int(input())
    r2 = int(input())

    dist_sq = (x1 - x2)**2 + (y1 - y2)**2
    rad_sq = (r1 + r2)**2

    if dist_sq < rad_sq:
        print("overlapping")
    else:
        print("no overlapping")

if __name__ == "__main__":
    main()
