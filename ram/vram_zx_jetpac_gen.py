# vram_jetpac_gen.py
# Maakt een Jetpac-achtige scene voor Gowin .mi (WIDTH=8, DEPTH=8192)
# Layout: 0..6143 = pixels, 6144..6911 = attributes, 6912..8191 = 0

WIDTH = 8
PIX_W, PIX_H = 256, 192
COLS, ROWS = 32, 24          # 8x8 cells
PIX_BYTES = COLS * ROWS * 8  # 6144
ATTR_BYTES = COLS * ROWS     # 768
TOTAL = 8192

# -----------------------------
# Minimal 8x8 font (digits + nodige letters)
# Bits: '1' = INK-pixel (linker bit = b7)
# -----------------------------
font8x8 = {
    '0': [0b00111100,0b01100110,0b01101110,0b01110110,0b01100110,0b01100110,0b00111100,0],
    '1': [0b00011000,0b00111000,0b00011000,0b00011000,0b00011000,0b00011000,0b00111100,0],
    '2': [0b00111100,0b01100110,0b00000110,0b00001100,0b00110000,0b01100000,0b01111110,0],
    '3': [0b00111100,0b01100110,0b00000110,0b00011100,0b00000110,0b01100110,0b00111100,0],
    '4': [0b00001100,0b00011100,0b00111100,0b01101100,0b01111110,0b00001100,0b00001100,0],
    '5': [0b01111110,0b01100000,0b01111100,0b00000110,0b00000100,0b01100110,0b00111100,0],
    '6': [0b00111100,0b01100110,0b01100000,0b01111100,0b01100110,0b01100110,0b00111100,0],
    '7': [0b01111110,0b00000110,0b00001100,0b00011000,0b00110000,0b00110000,0b00110000,0],
    '8': [0b00111100,0b01100110,0b01100110,0b00111100,0b01100110,0b01100110,0b00111100,0],
    '9': [0b00111100,0b01100110,0b01100110,0b00111110,0b00000110,0b01100110,0b00111100,0],

    'S': [0b00111110,0b01100000,0b01100000,0b00111100,0b00000110,0b00000110,0b01111100,0],
    'C': [0b00111100,0b01100110,0b01100000,0b01100000,0b01100000,0b01100110,0b00111100,0],
    'O': [0b00111100,0b01100110,0b01100110,0b01100110,0b01100110,0b01100110,0b00111100,0],
    'R': [0b01111100,0b01100110,0b01100110,0b01111100,0b01101100,0b01100110,0b01100110,0],
    'E': [0b01111110,0b01100000,0b01100000,0b01111100,0b01100000,0b01100000,0b01111110,0],
    'L': [0b01100000,0b01100000,0b01100000,0b01100000,0b01100000,0b01100000,0b01111110,0],
    'I': [0b00111100,0b00011000,0b00011000,0b00011000,0b00011000,0b00011000,0b00111100,0],
    'V': [0b01100110,0b01100110,0b01100110,0b01100110,0b00111100,0b00011000,0b00011000,0],
    # spatie
    ' ': [0,0,0,0,0,0,0,0],
}

# -----------------------------
# Hulpfuncties
# -----------------------------
def pix_addr(char_row, y_in_char, char_col):
    # Jouw lineaire layout: ((row*8 + y) * 32) + col
    return (char_row*8 + y_in_char) * COLS + char_col
    
def zx_addr(char_row, y_in_char, char_col):
    y = char_row*8 + y_in_char
    x_byte = char_col
    return((y & 0b00000111) << 8) | \
          ((y & 0b00111000) << 2) | \
          ((y & 0b11000000) << 5) | \
          x_byte

def set_cell_byte(img, char_col, char_row, y_in_char, byte_val):
    img[zx_addr(char_row, y_in_char, char_col)] = byte_val & 0xFF

def blit_char(img, ch, char_col, char_row):
    glyph = font8x8.get(ch, font8x8[' '])
    for y in range(8):
        set_cell_byte(img, char_col, char_row, y, glyph[y])

def blit_text(img, text, col, row):
    for i, ch in enumerate(text):
        blit_char(img, ch, col+i, row)

def draw_hline_cells(img, row, col0, col1, pattern=0xFF):
    for c in range(col0, col1+1):
        for y in range(8):
            set_cell_byte(img, c, row, y, pattern)

def blit_sprite(img, sprite_rows, col, row):
    # sprite_rows: list of rows, each row is 8-bit value (left=bit7)
    # height = len(sprite_rows), width = 8
    h = len(sprite_rows)
    for y in range(h):
        # plaats in juiste cell en y_in_char
        abs_y = row*8 + y
        char_row = abs_y // 8
        y_in_char = abs_y % 8
        set_cell_byte(img, col, char_row, y_in_char, sprite_rows[y])

def set_attr(attr, col, row, flash, bright, paper_rgb3, ink_rgb3):
    # bits: [7]=FLASH, [6]=BRIGHT, [5:3]=PAPER, [2:0]=INK
    val = ((1 if flash else 0) << 7) | ((1 if bright else 0) << 6) \
          | ((paper_rgb3 & 0x7) << 3) | (ink_rgb3 & 0x7)
    attr[row*COLS + col] = val & 0xFF

# Kleuren (3-bit RGB) conform Spectrum
COL_BLACK  = 0b000
COL_BLUE   = 0b001
COL_RED    = 0b010
COL_MAG    = 0b011
COL_GREEN  = 0b100
COL_CYAN   = 0b101
COL_YELLOW = 0b110
COL_WHITE  = 0b111

# -----------------------------
# Scene opbouwen
# -----------------------------
# Pixelbuffer (6144) en Attribute buffer (768)
img = [0]*PIX_BYTES
attr = [0]*ATTR_BYTES

# 1) Achtergrond: ruimte (blauw papier), sterren (witte stippen in de pixels)
#    Omdat attribute per 8x8 cel geldt: PAPER=BLUE, INK=WHITE (BRIGHT=1).
for r in range(ROWS):
    for c in range(COLS):
        set_attr(attr, c, r, flash=0, bright=1, paper_rgb3=COL_BLUE, ink_rgb3=COL_WHITE)

# Sterren: wat deterministisch “random” stippen (1 pixel per cel, soms 2)
def star_hash(x, y):
    # eenvoudig hashje voor deterministische pseudo-random
    v = (x*1103515245 + y*12345 + 0x9E3779B9) & 0xFFFFFFFF
    return v

for r in range(ROWS):
    for c in range(COLS):
        h = star_hash(c, r)
        # 0..7 = bitpositie (bit7 is links)
        if (h & 0x7) == 0:
            # één ster
            bitpos = (h >> 8) & 7
            mask = (1 << (7-bitpos))
            set_cell_byte(img, c, r, (h>>16) & 7, mask)
        elif (h & 0xF) == 0:
            # twee sterren
            bitpos1 = (h >> 8) & 7
            bitpos2 = (h >> 10) & 7
            y1 = (h>>16) & 7
            y2 = (h>>19) & 7
            set_cell_byte(img, c, r, y1, (1 << (7-bitpos1)))
            set_cell_byte(img, c, r, y2, (1 << (7-bitpos2)))

# 2) HUD bovenaan (rij 0..1): PAPER=BLUE, INK=WHITE (helder), tekst
blit_text(img, "SCORE 0000  LIVES 3", 2, 0)
# Maak HUD donkerder blauw papier maar bright tekst blijft zichtbaar; laten we BRIGHT=1 houden
for c in range(COLS):
    set_attr(attr, c, 0, flash=0, bright=1, paper_rgb3=COL_BLUE, ink_rgb3=COL_WHITE)
    set_attr(attr, c, 1, flash=0, bright=1, paper_rgb3=COL_BLUE, ink_rgb3=COL_WHITE)

# 3) Platform onderin (rij 20..21)
for r in [20, 21]:
    for c in range(2, 30):
        # PAPER=BLACK, INK=CYAN, geen bright (retro look)
        set_attr(attr, c, r, flash=0, bright=0, paper_rgb3=COL_BLACK, ink_rgb3=COL_CYAN)
        for y in range(8):
            # blok-vulling met afwisselend patroon
            pat = 0xFF if ((r+c) & 1) == 0 else 0x81
            set_cell_byte(img, c, r, y, pat)

# 4) Raket (midden): 16×24 → 2 kolommen × 3 cellen hoog
rocket = [
    0b00011000, 0b00111100, 0b01111110, 0b01111110, 0b01111110, 0b00111100, 0b00011000, 0,
    0b00011000, 0b00111100, 0b01111110, 0b01111110, 0b01111110, 0b00111100, 0b00011000, 0,
    0b00011000, 0b00111100, 0b01111110, 0b01111110, 0b01111110, 0b00111100, 0b00011000, 0,
]
# split in 3 blokken van 8 rijen
cx = 15; cy = 10  # cell-coords
for i in range(3):
    block = rocket[i*8:(i+1)*8]
    blit_sprite(img, block, cx, cy+i)
    blit_sprite(img, block, cx+1, cy+i)
    # Raket-attributes: PAPER=BLACK, INK=YELLOW, BRIGHT=1
    set_attr(attr, cx,   cy+i, 0, 1, COL_BLACK, COL_YELLOW)
    set_attr(attr, cx+1, cy+i, 0, 1, COL_BLACK, COL_YELLOW)

# 5) Speler links (8×16): INK=WHITE
player = [
    0b00011000,0b00111100,0b00111100,0b00111100,0b00011000,0b00111100,0b01111110,0b01011010,
    0b00011000,0b00111100,0b00111100,0b00111100,0b00011000,0b00111100,0b01111110,0b01011010,
]
px, py = 6, 12
blit_sprite(img, player[:8], px, py)
blit_sprite(img, player[8:], px, py+1)
set_attr(attr, px, py,   0, 1, COL_BLACK, COL_WHITE)
set_attr(attr, px, py+1, 0, 1, COL_BLACK, COL_WHITE)

# 6) Alien rechts (8×8): INK=MAGENTA
alien = [
    0b00111100,0b01111110,0b11011011,0b11111111,
    0b11111111,0b11011011,0b01111110,0b00111100
]
ax, ay = 24, 12
blit_sprite(img, alien, ax, ay)
set_attr(attr, ax, ay, 0, 1, COL_BLACK, COL_MAG)

# 7) Fuel can (8×8): INK=GREEN
fuel = [
    0b00111100,0b01111110,0b01100110,0b01111110,
    0b01100110,0b01100110,0b01111110,0b00111100
]
fx, fy = 12, 20
blit_sprite(img, fuel, fx, fy)
set_attr(attr, fx, fy, 0, 1, COL_BLACK, COL_GREEN)

# -----------------------------
# .mi uitschrijven
# -----------------------------
data = [0]*TOTAL
# 0..6143 pixels
for i in range(PIX_BYTES):
    data[i] = img[i]
# 6144..6911 attributes
for i in range(ATTR_BYTES):
    data[6144 + i] = attr[i]
# Rest 0

with open("vram_zx_jetpac.mi", "w") as f:
    f.write("WIDTH=8;\n")
    f.write(f"DEPTH={TOTAL};\n")
    f.write("ADDRESS_RADIX=HEX;\n")
    f.write("DATA_RADIX=HEX;\n")
    f.write("CONTENT BEGIN\n")
    for addr, b in enumerate(data):
        f.write(f"{addr:04X} : {b:02X};\n")
    f.write("END;\n")

print("vram_zx_jetpac.mi gegenereerd.")
