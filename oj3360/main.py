""" [LEARNING LOGS] หั่นขนมปัง """


def gaps(cuts, size):
    """ช่วงห่างระหว่างรอยตัดที่เรียงแล้ว รวมขอบ 0 และ size"""
    edges = [0] + cuts + [size]
    return [edges[i + 1] - edges[i] for i in range(len(edges) - 1)]


def main():
    """[LEARNING LOGS] หั่นขนมปัง"""
    w, h, m, n = map(int, input().split())
    xs = list(map(int, input().split()))
    ys = list(map(int, input().split()))
    widths = sorted(gaps(xs, w), reverse=True)
    heights = sorted(gaps(ys, h), reverse=True)
    # ชิ้นที่ใหญ่สุด/รองมาต้องมาจากคู่ (กว้างสุด, สูงสุด) หรือถัดไปอีกด้านละหนึ่ง
    cand = [widths[0] * heights[0]]
    if len(widths) > 1:
        cand.append(widths[1] * heights[0])
    if len(heights) > 1:
        cand.append(widths[0] * heights[1])
    cand.sort(reverse=True)
    print(cand[0], cand[1] if len(cand) > 1 else cand[0])


if __name__ == "__main__":
    main()
