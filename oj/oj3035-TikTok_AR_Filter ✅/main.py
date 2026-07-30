""" TikTok AR Filter """

def main():
    """TikTok AR Filter"""
    r, x, y = map(int, input().split())

    point_distance_sq = x**2 + y**2
    radius_sq = r**2

    if point_distance_sq < radius_sq:
        print("IN")
    elif point_distance_sq == radius_sq:
        print("ON")
    else:
        print("OUT")

if __name__ == "__main__":
    main()
