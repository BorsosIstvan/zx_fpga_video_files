WIDTH = 8
DEPTH = 8192

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

# Attribuutbyte (wit op zwart)
A_attr = 0b00000111  # bright white ink, black paper

# Maak leeg geheugen
ram = [0x00] * DEPTH

# Plaats de 8x8 A in linkerbovenhoek
start_addr = 0
stride = 8 * 32  # 8 rijen verder = 256 bytes

for row in range(8):
    addr = start_addr + row * stride
    ram[addr] = A_bitmap[row]

# Plaats attribuut (bovenste 8x8 blok, positie 0,0)
ram[6144] = A_attr

# Schrijf .mi bestand
with open("test_A.mi", "w") as f:
    f.write("WIDTH=8;\nDEPTH=8192;\nADDRESS_RADIX=HEX;\nDATA_RADIX=HEX;\nCONTENT BEGIN\n")
    for i in range(DEPTH):
        f.write(f"{i:04X} : {ram[i]:02X};\n")
    f.write("END;\n")

print("test_A.mi gegenereerd!")
