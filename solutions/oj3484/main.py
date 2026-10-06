""" หุ่นยนต์เคาะเสียงกระเบื้อง """


def main():
    """หุ่นยนต์เคาะเสียงกระเบื้อง"""
    first = input().split()
    n = int(first[0])
    p = float(first[1])
    grid = []
    for _ in range(n):
        grid.append(list(map(int, input().split())))
    col_tiles = [0] * n
    col_points = [0] * n
    total_tiles = 0
    total_points = 0
    for row in grid:
        tiles = 0
        points = 0
        for j in range(n):
            if row[j] > 0:
                tiles += 1
                col_tiles[j] += 1
            points += row[j]
            col_points[j] += row[j]
        total_tiles += tiles
        total_points += points
        print(" ".join(str(v) for v in row) + f" {tiles} {points}")
    print(" ".join(str(v) for v in col_tiles))
    print(" ".join(str(v) for v in col_points))
    print(f"{total_tiles} {total_points} {total_points * p:.2f}")


if __name__ == "__main__":
    main()
