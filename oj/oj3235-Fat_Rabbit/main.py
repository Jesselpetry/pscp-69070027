""" กระต่ายอ้วน """

def main():
    """กระต่ายอ้วน"""
    n = int(input())
    rabbits_names = []
    rabbits_wieght = []
    for _ in range(n):
        names,weight = input().split()
        rabbits_names.append(names)
        rabbits_wieght.append(int(weight))

    max_val = max(rabbits_wieght)
    max_index = rabbits_wieght.index(max_val)

    fat_rabbits = 0
    for i in range(n):
        if int(rabbits_wieght[i]) > 15:
            fat_rabbits += 1

    print(fat_rabbits)
    print(rabbits_names[max_index])

if __name__ == "__main__":
    main()
