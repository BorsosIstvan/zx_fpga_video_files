# ZX Spectrum scherminstellingen
WIDTH = 256
HEIGHT = 192
VRAM_SIZE = 6144
ATTR_SIZE = 768

# Lege RAM
ram = [0] * (VRAM_SIZE + ATTR_SIZE)

# Maak bitmap: 0=zwart, 1=wit
bitmap = [[0]*WIDTH for _ in range(HEIGHT)]

# Platformen tekenen
for y in (160, 144, 128):
    for x in range(50, 200):
        bitmap[y][x] = 1
        bitmap[y+1][x] = 1  # 2 pixels dik

# Raket tekenen in het midden
for y in range(140, 160):
    for x in range(120, 136):
        bitmap[y][x] = 1
bitmap[140][128] = 0  # puntje raket wit eruit voor detail

# Speler tekenen
for y in range(135, 145):
    for x in range(60, 70):
        bitmap[y][x] = 1
bitmap[135][65] = 0  # hoofd wit

# Zet bitmap om naar ZX Spectrum VRAM
for y in range(HEIGHT):
    for x_byte in range(32):
        byte = 0
        for bit in range(8):
            x = x_byte*8 + bit
            if bitmap[y][x]:
                byte |= (1 << (7-bit))
        # ZX Spectrum heeft een bijzondere adressing
        zx = ((y & 0x07) << 8) | ((y & 0x38) << 2) | ((y & 0xC0) << 5) | x_byte
        ram[zx] = byte

# Attribuut: wit op zwart
for row in range(24):
    for col in range(32):
        ram[VRAM_SIZE + row*32 + col] = 0x07  # INK=7 (wit), PAPER=0 (zwart)

# Schrijf .mi bestand
with open("jetpac_scene.mi", "w") as f:
    f.write("WIDTH=8;\nDEPTH=8192;\nADDRESS_RADIX=HEX;\nDATA_RADIX=HEX;\nCONTENT BEGIN\n")
    for addr, b in enumerate(ram):
        if b != 0:
            f.write(f"{addr:04X} : {b:02X};\n")
    f.write("END;\n")

print("jetpac_scene.mi gegenereerd!")
