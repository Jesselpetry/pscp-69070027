""" ไข้หวัดกระต่ายสายพันธุ์ใหม่ """


def calculate_risk(row, col, infected):
    """Calculate infection risk percentage for cell (row, col)."""
    highest_risk = 0
    for inf_r, inf_c in infected:
        distance = max(abs(row - inf_r), abs(col - inf_c))
        if not distance:
            return 100
        if distance == 1:
            highest_risk = max(highest_risk, 60)
        elif distance == 2:
            highest_risk = max(highest_risk, 20)
    return highest_risk


def main():
    """ไข้หวัดกระต่ายสายพันธุ์ใหม่"""
    rows, cols = map(int, input().split())
    my_r, my_c = map(int, input().split())
    num_infected = int(input().strip())

    infected = []
    for _ in range(num_infected):
        inf_r, inf_c = map(int, input().split())
        infected.append((inf_r, inf_c))

    safe_count = 0
    for r in range(rows):
        for c in range(cols):
            if not calculate_risk(r, c, infected):
                safe_count += 1

    my_risk = calculate_risk(my_r, my_c, infected)
    print(safe_count)
    print(f"{my_risk}%")


if __name__ == "__main__":
    main()
