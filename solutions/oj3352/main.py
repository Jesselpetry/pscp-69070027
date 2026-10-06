""" LastStand """
import json


def main():
    """LastStand"""
    raw = input().strip()
    try:
        items = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        clean = raw.strip("[]")
        items = [x.strip() for x in clean.split(",") if x.strip()]

    for item in items:
        print(abs(int(item)) % 10)


if __name__ == "__main__":
    main()
