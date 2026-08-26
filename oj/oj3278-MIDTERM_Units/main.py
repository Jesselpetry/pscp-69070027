""" Units """

def main():
    """Units"""
    value = float(input())
    target_unit = input().strip()
    source_unit = input().strip()

    if source_unit == "NIU":
        niu = value
    elif source_unit == "KUEP":
        niu = value * 12
    elif source_unit == "SOK":
        niu = value * 24
    elif source_unit == "WA":
        niu = value * 96
    else:
        niu = value * 1920

    if target_unit == "NIU":
        answer = niu
    elif target_unit == "KUEP":
        answer = niu / 12
    elif target_unit == "SOK":
        answer = niu / 24
    elif target_unit == "WA":
        answer = niu / 96
    else:
        answer = niu / 1920

    print(f"{answer:.4f}")

if __name__ == "__main__":
    main()
