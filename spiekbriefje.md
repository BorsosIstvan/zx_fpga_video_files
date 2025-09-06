# Git & GitHub Spiekbriefje voor nieuw project

## Nieuwe GitHub repo maken & koppelen aan lokale map

1. **Maak map en ga erheen**
```bash
mkdir zx-spectrum-fpga
cd zx-spectrum-fpga
```

2. **Kopieer je projectbestanden in deze map**  
   Bijvoorbeeld `myhdmi` map of andere bestanden.

3. **Initialiseer Git**
```bash
git init
```

4. **Voeg alle bestanden toe**
```bash
git add .
```

5. **Commit je bestanden**
```bash
git commit -m "Initial commit: voeg projectbestanden toe"
```

6. **Maak nieuwe repo aan op GitHub**  
   Ga naar [github.com/new](https://github.com/new)  
   Naam: `zx-spectrum-fpga`  
   Maak repo aan.

7. **Koppel lokale repo aan GitHub**
```bash
git remote add origin https://github.com/jouwgebruikersnaam/zx-spectrum-fpga.git
```

8. **Push je commit naar GitHub**
```bash
git branch -M main
git push -u origin main
```

---

## Bestanden updaten en pushen

- Na wijzigingen:
```bash
git status          # Bekijk gewijzigde bestanden
git add .           # Voeg toe aan commit
git commit -m "je bericht"  # Commit wijzigingen
git push            # Upload naar GitHub
```

---

## Handige commando's

- `git status` — toont welke bestanden gewijzigd zijn en niet zijn gecommit  
- `git log` — toont de geschiedenis van commits  
- `git pull` — haalt updates op van GitHub naar lokaal  
- `git remote -v` — toont de gekoppelde remote URL's  

---

**Tip:** Gebruik altijd duidelijke commit berichten zoals `"Fix HDMI timing"` of `"Update README.md"` zodat je makkelijk kan terugvinden wat er is veranderd.

---

Succes met je project! 🚀
