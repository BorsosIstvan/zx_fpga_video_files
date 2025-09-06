import sys

TOTAL = 8192  # aantal bytes pixeldata

def linear_to_zx(data):
    zx_data = [0] * TOTAL
    for pixel_addr, b in enumerate(data):
        x = pixel_addr & 0x1F          # bits 0..4
        y = (pixel_addr >> 5) & 0x07   # bits 5..7
        g = (pixel_addr >> 8) & 0x03   # bits 8..9
        zx_addr = (g << 8) | (y << 5) | x
        zx_data[zx_addr] = b
    return zx_data

def main():
    if len(sys.argv) != 3:
        print("Usage: python linear2zx.py input.mi output.mi")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    header = []
    data = []

    with open(input_file, "r") as f:
        in_content = False
        for line in f:
            line = line.strip()
            if line.startswith("CONTENT BEGIN"):
                in_content = True
                continue
            if line.startswith("END;"):
                in_content = False
                continue
            if not in_content:
                header.append(line)
            else:
                # regel zoals: 0000 : FF;
                addr_part, byte_part = line.split(":")
                byte_val = int(byte_part.strip().rstrip(";"), 16)
                data.append(byte_val)

    if len(data) != TOTAL:
        print(f"Waarschuwing: verwacht {TOTAL} bytes, gevonden {len(data)} bytes")

    zx_data = linear_to_zx(data)

    with open(output_file, "w") as f:
        for line in header:
            f.write(line + "\n")
        f.write("CONTENT BEGIN\n")
        for addr, b in enumerate(zx_data):
            f.write(f"{addr:04X} : {b:02X};\n")
        f.write("END;\n")

    print(f"{output_file} gegenereerd.")

if __name__ == "__main__":
    main()
