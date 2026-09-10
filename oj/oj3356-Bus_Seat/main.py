""" Bus Seat """


def main():
    """Bus Seat"""
    per_row = int(input())               # ที่นั่งต่อแถว (เลขคู่)
    rows = int(input())                  # จำนวนแถวในรถ (คอลัมน์ของผัง)
    mine = int(input())                  # หมายเลขที่นั่งของนาย ก

    blocks = []
    # ที่นั่งจับเป็นคู่ ๆ มีทางเดินคั่นระหว่างคู่ พิมพ์จากคู่บนสุดลงล่าง
    for top in range(per_row - 1, 0, -2):
        block = []
        for p in (top, top - 1):         # p = ลำดับที่นั่งในคอลัมน์ (0 = ล่างสุด)
            cells = []
            for c in range(1, rows + 1):
                seat = (c - 1) * per_row + p + 1
                cells.append("XX" if seat == mine else f"{seat:02d}")
            block.append(" ".join(cells))
        blocks.append("\n".join(block))
    print("\n\n".join(blocks))            # บรรทัดว่าง = ทางเดินระหว่างคู่


if __name__ == "__main__":
    main()
