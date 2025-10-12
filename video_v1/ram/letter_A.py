# ZX Spectrum: 256x192 pixels = 6144 bytes bitmap
# Attributen = 32x24 blokken = 768 bytes? Maar voor MI vullen we 8192 = 6144+2048
bitmap = [0] * 6144  # lege bitmap
attributes = [0x07] * 2048  # testkleur: wit op zwart (attribuut 0x07)

# 8x8 letter A
letter_A = [
    0b00111100,
    0b01000010,
    0b10000001,
    0b11111111,
    0b10000001,
    0b10000001,
    0b10000001,
    0b00000000,
]

# ZX Spectrum VRAM-adressering voor bitmap
def zx_address(x_byte, y):
    return (y & 0x07) + ((y & 0x38) << 2) + ((y & 0xC0) << 5) + x_byte

# Plaats letter A op x_byte=0, y=0
x_byte = 0
y_start = 0
for row, byte in enumerate(letter_A):
    addr = zx_address(x_byte, y_start + row)
    bitmap[addr] = byte

# Combineer bitmap + attributes
data = bitmap + attributes  # totaal 8192 bytes

# Schrijf .mi bestand
with open("letter_A.mi", "w") as f:
    f.write("WIDTH=8;\n")
    f.write("DEPTH=8192;\n")
    f.write("ADDRESS_RADIX=HEX;\n")
    f.write("DATA_RADIX=HEX;\n")
    f.write("CONTENT BEGIN\n")
    for i, b in enumerate(data):
        f.write(f"{i:04X} : {b:02X};\n")
    f.write("END;\n")

print("letter_A.mi gegenereerd!")
