""" [LEARNING LOGS] Giraffe """


def main():
    """[LEARNING LOGS] Giraffe"""
    n = int(input())
    h = [int(input()) for _ in range(n)]
    count = 0
    for i in range(n):
        taller_left = i == 0 or h[i] > h[i - 1]
        taller_right = i == n - 1 or h[i] > h[i + 1]
        if taller_left and taller_right:   # สูงกว่าเพื่อนทั้งซ้ายและขวา
            count += 1
    print(count)


if __name__ == "__main__":
    main()
