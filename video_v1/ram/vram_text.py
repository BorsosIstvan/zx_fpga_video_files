# gen_spectrum_text.mi.py
# Genereert een ZX Spectrum style .mi (8192 bytes)
# Geen imports, alleen standaard Python

# 8x8 font (gebruik jouw opgegeven bytes)
font8x8 = {
    '0': [0x3C,0x66,0x6E,0x76,0x66,0x66,0x3C,0x00],
    '1': [0x18,0x38,0x18,0x18,0x18,0x18,0x3C,0x00],
    '2': [0x3C,0x66,0x06,0x0C,0x30,0x60,0x7E,0x00],
    '3': [0x3C,0x66,0x06,0x1C,0x06,0x66,0x3C,0x00],
    '4': [0x0C,0x1C,0x3C,0x6C,0x7E,0x0C,0x0C,0x00],
    '5': [0x7E,0x60,0x7C,0x06,0x06,0x66,0x3C,0x00],
    '6': [0x3C,0x66,0x60,0x7C,0x66,0x66,0x3C,0x00],
    '7': [0x7E,0x06,0x0C,0x18,0x30,0x30,0x30,0x00],
    '8': [0x3C,0x66,0x66,0x3C,0x66,0x66,0x3C,0x00],
    '9': [0x3C,0x66,0x66,0x3E,0x06,0x66,0x3C,0x00],
    'A': [0x18,0x3C,0x66,0x66,0x7E,0x66,0x66,0x00],
    'B': [0x7C,0x66,0x66,0x7C,0x66,0x66,0x7C,0x00],
    'C': [0x3C,0x66,0x60,0x60,0x60,0x66,0x3C,0x00],
    'D': [0x78,0x6C,0x66,0x66,0x66,0x6C,0x78,0x00],
    'E': [0x7E,0x60,0x60,0x7C,0x60,0x60,0x7E,0x00],
    'F': [0x7E,0x60,0x60,0x7C,0x60,0x60,0x60,0x00],
    ' ': [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
}

# Tekstregel die we willen tonen (max 32 chars)
teks = list('0123456789ABCDEF     DEF A12 CAD')  # je voorbeeld; wordt op row 0 geplaatst

# Spectrum screen layout constants
COLS = 32
ROWS = 24
PIX_W = 256
PIX_H = 192
PIX_BYTES = 6144
ATTR_BYTES = 768
TOTAL = 8192

# helper: compute linear pixel index (y_total * 32 + x_byte)
def linear_pix_index(char_row, y_in_char, char_col):
    # char_row: 0..23 (which 8-row block)
    # y_in_char: 0..7 (line inside the character)
    # char_col: 0..31
    y_total = char_row * 8 + y_in_char  # 0..191
    return y_total * COLS + char_col    # 0..6143

# ZX scrambled address mapping function (y-bits shuffled)
def linear_to_zxaddr(linear_index):
    # linear_index = y_total * 32 + x (0..6143)
    x = linear_index & 0x1F            # bits [4:0]
    y = (linear_index >> 5) & 0xFF     # y_total 0..191 in low bits
    # ZX mapping:
    # zx = (y[2:0] << 8) | (y[5:3] << 5?) wait careful:
    # use formula: (y & 0x07)<<8 | (y & 0x38)<<2 | (y & 0xC0)<<5 | x
    zx = ((y & 0x07) << 8) | ((y & 0x38) << 2) | ((y & 0xC0) << 5) | x
    # result is 0..6143
    return zx

# Prepare full memory (all zeros)
mem = [0] * TOTAL

# 1) Fill pixel bytes (0..6143) with our text in char cells
# Place teks on row 0 starting at col 0
row0 = 0
for i, ch in enumerate(teks):
    if i >= COLS:
        break
    ch_up = ch.upper()
    glyph = font8x8.get(ch_up, font8x8[' '])  # 8 bytes
    for y_in_char in range(8):
        linear = linear_pix_index(row0, y_in_char, i)
        zxaddr = linear_to_zxaddr(linear)
        # store glyph byte at zxaddr
        mem[zxaddr] = glyph[y_in_char] & 0xFF

# 2) Fill attribute bytes (6144..6911)
# We'll set BRIGHT=1, PAPER=BLACK (0), INK=WHITE (7) -> attr = 0b01000111 = 0x47
attr_val = (1 << 6) | (0 << 3) | 0x07  # bright, paper=0, ink=7
for r in range(ROWS):
    for c in range(COLS):
        mem[PIX_BYTES + r*COLS + c] = attr_val

# 3) Rest (6912..8191) already zero

# 4) Write .mi file
with open("vram_text.mi", "w") as f:
    f.write("WIDTH=8;\n")
    f.write("DEPTH=%d;\n" % TOTAL)
    f.write("ADDRESS_RADIX=HEX;\n")
    f.write("DATA_RADIX=HEX;\n")
    f.write("CONTENT BEGIN\n")
    for addr, b in enumerate(mem):
        f.write("%04X : %02X;\n" % (addr, b))
    f.write("END;\n")

print("vram_text.mi gegenereerd (8192 bytes).")
