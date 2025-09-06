# ZX FPGA Video Files  

## 🇳🇱 Beschrijving  
Dit project bevat de FPGA-video-modules voor de **ZX Spectrum-implementatie op de Tang Nano 9K**.  
Het doel is om een werkende ZX Spectrum te bouwen die beeld kan tonen op een modern HDMI-scherm (LCD/TV).  

### Kenmerken  
- **Klokgenerator (Gowin)**:  
  - Genereert **125 MHz** uit de ingebouwde **27 MHz oscillator** van de Tang Nano 9K.  
  - Met **clkdiv** wordt 25 MHz afgeleid (125 / 5).  

- **HDMI-output**:  
  - TMDS encoder inbegrepen.  
  - Timing flow voor **1024×768 @ 70 Hz**.  
  - `.cst` constraints-bestand voor koppeling van HDMI-signalen (resetn, 27 MHz klok, differentiële HDMI-klok en RGB).  

- **ULA (ula_my.v)**:  
  - Werkt op **3,5 MHz**.  
  - Genereert **busy**, **hcount** en **vcount** volgens klassieke ZX Spectrum timing (488×312 totaal, 256×192 actief).  
  - **Busy** is actief in het zichtbare gedeelte van het beeld.  

- **Video RAM pipeline (video_ram_datapijp.v)**:  
  - Kopieert beelddata vanuit een **single-port RAM (SPRAM)** naar een **dual-port RAM (SDPB)**.  
  - **Port A** = input (data van ULA).  
  - **Port B** = output (data naar HDMI).  

### Repository-inhoud  
- `clk125.v` – Gowin klokgenerator (27 MHz → 125 MHz)  
- `clkdiv.v` – Klokdeler voor 25 MHz  
- `tmds_encoder.v` – HDMI TMDS encoder  
- `video_timing.v` – HDMI timing generator (1024×768 @ 70 Hz)  
- `video_ram_datapijp.v` – RAM pipeline (SPRAM → dual RAM → HDMI)  
- `ula_my.v` – ZX Spectrum ULA-timing (3,5 MHz, busy/h/v-count)  
- `video_card_top.v` – Topmodule met alle componenten  
- `zx_fpga_video_files.cst` – Constraints-bestand voor Tang Nano 9K  

### Doel  
Een werkende **ZX Spectrum in FPGA (Tang Nano 9K)**, die via HDMI een beeld toont op moderne LCD/TV-schermen.  

---

## 🇬🇧 Description  
This project contains the FPGA video modules for the **ZX Spectrum implementation on the Tang Nano 9K**.  
The goal is to build a working ZX Spectrum that can output video to a modern HDMI display (LCD/TV).  

### Features  
- **Clock generator (Gowin)**:  
  - Generates **125 MHz** from the built-in **27 MHz oscillator** of the Tang Nano 9K.  
  - **clkdiv** provides 25 MHz (125 / 5).  

- **HDMI output**:  
  - Includes TMDS encoder.  
  - Timing flow for **1024×768 @ 70 Hz**.  
  - `.cst` constraints file connects HDMI signals (resetn, 27 MHz clock, differential HDMI clock, RGB).  

- **ULA (ula_my.v)**:  
  - Runs at **3.5 MHz**.  
  - Generates **busy**, **hcount**, and **vcount** according to ZX Spectrum timing (488×312 total, 256×192 active).  
  - **Busy** is active during the visible part of the frame.  

- **Video RAM pipeline (video_ram_datapijp.v)**:  
  - Copies video data from **single-port RAM (SPRAM)** into a **dual-port RAM (SDPB)**.  
  - **Port A** = input (ULA data).  
  - **Port B** = output (to HDMI).  

### Repository contents  
- `clk125.v` – Gowin clock generator (27 MHz → 125 MHz)  
- `clkdiv.v` – Clock divider for 25 MHz  
- `tmds_encoder.v` – HDMI TMDS encoder  
- `video_timing.v` – HDMI timing generator (1024×768 @ 70 Hz)  
- `video_ram_datapijp.v` – RAM pipeline (SPRAM → dual RAM → HDMI)  
- `ula_my.v` – ZX Spectrum ULA timing (3.5 MHz, busy/h/v-count)  
- `video_card_top.v` – Top module with all components  
- `zx_fpga_video_files.cst` – Constraints file for Tang Nano 9K  

### Goal  
A working **ZX Spectrum in FPGA (Tang Nano 9K)**, displaying video over HDMI on modern LCD/TV screens.  

---

## 🇭🇺 Leírás  
Ez a projekt a **ZX Spectrum FPGA videómoduljait** tartalmazza, Tang Nano 9K platformon.  
A cél egy működő ZX Spectrum megvalósítása FPGA-ban, amely HDMI-n keresztül modern LCD/TV kijelzőre ad képet.  

### Jellemzők  
- **Órajel-generátor (Gowin)**:  
  - **125 MHz** órajelet állít elő a Tang Nano 9K beépített **27 MHz-es oszcillátorából**.  
  - A **clkdiv** modul 25 MHz-et biztosít (125 / 5).  

- **HDMI kimenet**:  
  - TMDS kódolóval.  
  - Időzítési modul **1024×768 @ 70 Hz** felbontásra.  
  - `.cst` fájl tartalmazza a HDMI jelek hozzárendelését (resetn, 27 MHz órajel, differenciális HDMI órajel, RGB).  

- **ULA (ula_my.v)**:  
  - **3,5 MHz** frekvencián fut.  
  - Generálja a **busy**, **hcount** és **vcount** jeleket a klasszikus ZX Spectrum időzítésnek megfelelően (összesen 488×312, aktív kép 256×192).  
  - A **busy** jel az aktív képrészben van érvényben.  

- **Video RAM pipeline (video_ram_datapijp.v)**:  
  - Képadatokat másol egy **single-port RAM (SPRAM)**-ból egy **dual-port RAM (SDPB)**-ba.  
  - **Port A** = bemenet (ULA adat).  
  - **Port B** = kimenet (HDMI felé).  

### Repository tartalma  
- `clk125.v` – Gowin órajel-generátor (27 MHz → 125 MHz)  
- `clkdiv.v` – Órajelosztó 25 MHz-re  
- `tmds_encoder.v` – HDMI TMDS kódoló  
- `video_timing.v` – HDMI időzítés (1024×768 @ 70 Hz)  
- `video_ram_datapijp.v` – RAM pipeline (SPRAM → dual RAM → HDMI)  
- `ula_my.v` – ZX Spectrum ULA időzítés (3,5 MHz, busy/h/v-count)  
- `video_card_top.v` – Top modul minden komponenssel  
- `zx_fpga_video_files.cst` – Constraints fájl Tang Nano 9K-hoz  

### Cél  
Egy működő **ZX Spectrum FPGA-ban (Tang Nano 9K)**, amely HDMI-n keresztül jeleníti meg a képet modern LCD/TV kijelzőkön.  
