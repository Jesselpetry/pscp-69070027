""" ราศี """

def main():
    """ราศี"""
    day = int(input())
    month = int(input())

    signs = (
        "capricorn", "aquarius", "pisces", "aries",
        "taurus", "gemini", "cancer", "leo",
        "virgo", "libra", "scorpio", "sagittarius"
    )
    cutoffs = (19, 18, 20, 19, 20, 21, 22, 22, 22, 23, 21, 21)

    if day <= cutoffs[month - 1]:
        print(signs[month - 1])
    else:
        print(signs[month % 12])

if __name__ == "__main__":
    main()
