""" Suvarnabhumi Airport Parking """

RATES = {
    1: 25,
    2: 50,
    3: 80,
    4: 110,
    5: 145,
    6: 180,
}


def main():
    """Suvarnabhumi Airport Parking"""
    try:
        in_hour_str, in_min_str = input().strip().split(".")
        out_hour_str, out_min_str = input().strip().split(".")
        h_in, m_in = int(in_hour_str), int(in_min_str)
        h_out, m_out = int(out_hour_str), int(out_min_str)
    except (ValueError, TypeError):
        print("ERROR")
        return

    valid_in = (0 <= h_in <= 23) and (0 <= m_in <= 59)
    valid_out = (0 <= h_out <= 23) and (0 <= m_out <= 59)
    if not (valid_in and valid_out):
        print("ERROR")
        return

    enter_total = h_in * 60 + m_in
    exit_total = h_out * 60 + m_out

    if exit_total < enter_total:
        print("ERROR")
        return

    stay_minutes = exit_total - enter_total
    if stay_minutes <= 15:
        print("FREE")
        return

    hours = (stay_minutes + 59) // 60
    if hours in RATES:
        print(RATES[hours])
    elif hours <= 24:
        print(250)
    else:
        print("ERROR")


if __name__ == "__main__":
    main()
