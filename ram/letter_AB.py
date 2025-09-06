WIDTH = 8
DEPTH = 8192

# Spectrum screen layout constants
COLS = 32
ROWS = 24
PIX_W = 256
PIX_H = 192
PIX_BYTES = 6144
ATTR_BYTES = 768
TOTAL = 8192

# 8x8 bitmap van 'A'
A_bitmap = [
    0b00011000,
    0b00100100,
    0b01000010,
    0b01000010,
    0b01111110,
    0b01000010,
    0b01000010,
    0b00000000
]

B_bitmap = [
    0b01111100,
    0b01000010,
    0b01000010,
    0b01111100,
    0b01000010,
    0b01000010,
    0b01111100,
    0b00000000
]

C_bitmap = [
    0b00111100,
    0b01000010,
    0b01000000,
    0b01000000,
    0b01000000,
    0b01000010,
    0b00111100,
    0b00000000
]

D_bitmap = [
    0b01111100,
    0b01000010,
    0b01000010,
    0b01000010,
    0b01000010,
    0b01000010,
    0b01111100,
    0b00000000
]

E_bitmap = [
    0b01111110,
    0b01000000,
    0b01000000,
    0b01111100,
    0b01000000,
    0b01000000,
    0b01111110,
    0b00000000
]

# Attribuutbyte (wit op zwart)
A_attr = 0b00000111  # bright white ink, black paper
B_attr = 0b11011100

# Maak leeg geheugen
ram = [0x00] * DEPTH

# Plaats de 8x8 A in linkerbovenhoek
start_addr = 0
stride = 8 * 32  # 8 rijen verder = 256 bytes

def zx_addr(x, y):
    # x = 0..31 (byte-kolom), y = 0..191 (pixelrij)
    return ((y & 0b111) << 8) | ((y & 0b111000) << 2) | ((y & 0b11000000) << 5) | x


for row in range(8):
    addr = zx_addr(0, 0*8 + row)  # x=0 kolom, y_base start-rij
    ram[addr] = A_bitmap[row]
	
for row in range(8):
    addr = zx_addr(0, 12*8 + row)
    ram[addr] = B_bitmap[row]
    
for row in range(8):
    addr = zx_addr(0, 14*8 + row)
    ram[addr] = C_bitmap[row]
    
for row in range(8):
    addr = zx_addr(0, 16*8 + row)
    ram[addr] = D_bitmap[row]
    
for row in range(8):
    addr = zx_addr(0, 23*8 + row)
    ram[addr] = E_bitmap[row]

# Plaats attribuut (bovenste 8x8 blok, positie 0,0)
#ram[6144] = A_attr
#ram[6145] = A_attr

for i in range(768):
    ram[6144 + i] = A_attr
    
ram[6144] = B_attr

# Schrijf .mi bestand
with open("test_AB.mi", "w") as f:
    f.write("WIDTH=8;\nDEPTH=8192;\nADDRESS_RADIX=HEX;\nDATA_RADIX=HEX;\nCONTENT BEGIN\n")
    for i in range(DEPTH):
        f.write(f"{i:04X} : {ram[i]:02X};\n")
    f.write("END;\n")

print("test_AB.mi gegenereerd!")