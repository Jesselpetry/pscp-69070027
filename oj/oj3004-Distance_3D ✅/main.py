""" หาระยะทางระหว่างจุด 3D """
import math as m

def main():
    """หาระยะทางระหว่างจุด 3D"""
    po1 = str(input())
    po2 = str(input())
    poi1 = po1.split(" ")
    poi2 = po2.split(" ")

    x1 = int(poi1[0])
    y1 = int(poi1[1])
    z1 = int(poi1[2])

    x2 = int(poi2[0])
    y2 = int(poi2[1])
    z2 = int(poi2[2])

    vals = [x1, y1, z1, x2, y2, z2]

    if all(-200000 <= v <= 200000 for v in vals):
        print(f"{m.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2):.2f}")

if __name__ == "__main__":
    main()
