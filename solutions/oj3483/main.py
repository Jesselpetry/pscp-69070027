""" มาเป็นทีม """


def main():
    """มาเป็นทีม"""
    n, m = map(int, input().split())
    if not (1 <= n <= 10 and 1 <= m <= 20):
        print("Data Incorrect")
        return
    teams = []
    for _ in range(n):
        row = list(map(int, input().split()))
        teams.append(row)
    for row in teams:
        if len(row) != m or any(s < 0 or s > 100 for s in row):
            print("Data Incorrect")
            return
    total = 0
    for i, row in enumerate(teams, 1):
        avg = sum(row) / m
        total += sum(row)
        print(f"Team {i}: Average = {avg:.2f}, Max = {max(row)}")
    print(f"Total Score of All Teams = {total}")


if __name__ == "__main__":
    main()
