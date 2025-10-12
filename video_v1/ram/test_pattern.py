WIDTH = 256
HEIGHT = 192
VRAM_SIZE = 6144
ATTR_SIZE = 768

# Leeg VRAM
ram = [0] * (VRAM_SIZE + ATTR_SIZE)

# Testpatroon: verticale strepen
bitmap = [[(x//8) % 2 for x in range(WIDTH)] for y in range(HEIGHT)]

# Zet bitmap om naar Spectrum VRAM
for y in range(HEIGHT):
    for x_byte in range(32):
        byte = 0
        for bit in range(8):
            x = x_byte*8 + bit
            if bitmap[y][x]:
                byte |= (1 << (7-bit))
        # Spectrum adresberekening
        zx = ((y & 0x07) << 8) | ((y & 0x38) << 2) | ((y & 0xC0) << 5) | x_byte
        ram[zx] = byte

# Attribuut: wisselende kleuren voor testen
for row in range(24):
    for col in range(32):
        ram[VRAM_SIZE + row*32 + col] = (row % 8)  # INK = 0..7, PAPER=0

# Schrijf .mi bestand
with open("test_pattern.mi", "w") as f:
    f.write("WIDTH=8;\nDEPTH=8192;\nADDRESS_RADIX=HEX;\nDATA_RADIX=HEX;\nCONTENT BEGIN\n")
    for addr, b in enumerate(ram):
        if b != 0:
            f.write(f"{addr:04X} : {b:02X};\n")
    f.write("END;\n")

print("test_pattern.mi gegenereerd!")
