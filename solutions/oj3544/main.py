""" ระบบจัดการคลังสินค้า """


def main():
    """ระบบจัดการคลังสินค้า"""
    stock = {}
    out = []
    while True:
        parts = input().split()
        if not parts:
            continue
        cmd = parts[0]
        if cmd == "END":
            break
        if cmd == "ADD":
            name = parts[1]
            qty = int(parts[2])
            stock[name] = stock.get(name, 0) + qty
        elif cmd == "REMOVE":
            name = parts[1]
            qty = int(parts[2])
            current = stock.get(name, 0)
            if current >= qty:
                stock[name] = current - qty
            else:
                stock[name] = 0
                out.append("Not enough stock for " + name)
        elif cmd == "CHECK":
            low = sorted(n for n in stock if stock[n] < 5)
            if low:
                for n in low:
                    out.append(n)
            else:
                out.append("All stocks are sufficient")
        elif cmd == "REPORT":
            for n in sorted(stock):
                out.append(n + ": " + str(stock[n]))
    print("\n".join(out))


if __name__ == "__main__":
    main()
