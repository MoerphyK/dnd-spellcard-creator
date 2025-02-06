
# DnD Spell Cards Generator

Dieses Projekt generiert beidseitige Spielkarten (ähnlich denen von Magic: The Gathering oder Hearthstone) für Dungeons & Dragons 5e-Spells auf Basis einer CSV-Datei. Mithilfe von Python, [Pillow](https://pillow.readthedocs.io/) und [ReportLab](https://www.reportlab.com/) werden die Karten als PNGs erstellt und anschließend in ein PDF konvertiert – so dass sie doppelseitig (Vorder- und Rückseite) ausgedruckt werden können.

## Features

- **Automatisierte Karten-Erstellung:**  
  Lese Spell-Daten aus einer CSV-Datei und kombiniere diese mit vorbereiteten grafischen Assets (Hintergründe, Banner, Illustrationen, Klassen-Symbole, etc.) zu fertigen Karten.

- **Dynamische Textplatzierung:**  
  Mittels dynamischer Fontgrößen-Anpassung (inklusive automatischem Zeilenumbruch und Anpassung des Wrap-Parameters) wird der verfügbare Platz in den Textboxen optimal ausgenutzt.

- **PDF-Erstellung für doppelseitigen Druck:**  
  Die erzeugten A7-Karten werden in einem A4-PDF in einem 2×2-Raster angeordnet – mit angepasster Reihenfolge für die Vorder- und Rückseite, sodass die Karten beim doppelseitigen Druck exakt übereinanderliegen.

## Projektstruktur

```
.
├── assets
│   ├── front_background.png
│   ├── back_background.png
│   ├── spellname_banner.png
│   ├── illustration.png
│   ├── front_frame.png
│   ├── fonts
│   │   └── UNISPACE_BD.ttf
│   └── class_banners
│       ├── barbarian.png
│       ├── bard.png
│       ├── cleric.png
│       ├── ... (weitere Klassenbanner)
├── csv
│   └── spells.csv
├── output
│   ├── [Generierte PNGs (Front- und Rückseiten)]
│   └── cards_double_sided.pdf
└── create_cards.py
```

- **assets/** – Enthält alle grafischen Vorlagen:
  - Hintergründe, Banner, Illustrationen, Rahmen und Klassenbanner.
  - Unter `assets/fonts/` befindet sich die verwendete TTF-Datei (hier `UNISPACE_BD.ttf`).

- **csv/** – Beinhaltet die CSV-Datei (`spells.csv`) mit den Spell-Daten.  
  - Die CSV muss Spalten wie `Name`, `Casting Time`, `Duration`, `Range`, `Components`, `Classes`, `Text` und `At Higher Levels` enthalten.
  - Die Datei wurde von der DnD Seite https://5e.tools/spells heruntergeladen.

- **output/** – Hier werden alle generierten PNG-Dateien abgelegt.

- **pdf/** - Hier werden alle generierten PDF-Dateien abgelegt.

- **main.py** – Das Hauptskript, das:
  1. Die Assets und die CSV-Daten einliest.
  2. Die Karten (Vorder- und Rückseiten) erstellt, wobei dynamisch die optimale Fontgröße ermittelt wird.

- **pdf.py** - Das PDF Skript, das: 
    1. Die erzeugten Karten in ein PDF (im A4-Format) zusammenfügt, sodass beim doppelseitigen Druck Vorder- und Rückseite korrekt zueinander passen.

- **pdf_a7.py** - Das PDF Skript, das: 
    1. Die erzeugten Karten in ein PDF (im A7-Format) aneinanderreiht, sodass jede Seite der PDF eine Karten-Vorder oder -Rückseite darstellt.


## Voraussetzungen

- Python 3.x  
- [Pillow](https://pillow.readthedocs.io/) – Bildverarbeitung (Installation: `pip install pillow`)
- [ReportLab](https://www.reportlab.com/) – PDF-Generierung (Installation: `pip install reportlab`)

## Installation

1. **Klone das Repository** (oder lade die Dateien herunter):
   ```bash
   git clone https://github.com/dein-benutzername/dnd-spell-cards.git
   cd dnd-spell-cards
   ```

2. **Installiere die benötigten Python-Pakete:**
   ```bash
   pip install pillow reportlab
   ```

## Verwendung

1. **CSV vorbereiten:**  
   Stelle sicher, dass sich die CSV-Datei (`spells.csv`) im Ordner `csv` befindet und die benötigten Spalten enthält.
   Die CSV Datei besteht aus 

2. **Assets anpassen:**  
   Lege alle erforderlichen PNGs (Hintergründe, Banner, Illustrationen, etc.) in den entsprechenden Unterordnern im Ordner `assets` ab.

3. **Karten erstellen:**  
   Führe das Skript aus:
   ```bash
   python create_cards.py
   ```
   - Das Skript erzeugt für jeden Spell im CSV-Dokument zwei PNGs (Front- und Rückseite) im Ordner `output`.
   - Anschließend wird ein PDF (`cards_double_sided.pdf`) erstellt, in dem die Karten so angeordnet sind, dass beim doppelseitigen Druck die Vorderseiten in der Reihenfolge  
     ```
     1  2
     3  4
     ```
     und die Rückseiten in der Reihenfolge  
     ```
     2  1
     4  3
     ```
     erscheinen.

4. **Doppelseitiger Druck:**  
   Beim Drucken des PDFs stelle sicher, dass die Druckeinstellungen (z. B. "lange Seite gebunden" bzw. "Buchdruck") korrekt sind, damit Vorder- und Rückseite exakt übereinander liegen.

## Anpassungsmöglichkeiten

- **Dynamische Fontgröße:**  
  Die Funktionen `find_optimal_font_size` und `draw_text_left_aligned_at` passen die Schriftgröße dynamisch an den verfügbaren Platz in den Textboxen an.  
  Du kannst Parameter wie `min_font_size`, `max_font_size`, `line_spacing` und `paragraph_spacing` direkt im Code anpassen.

- **Wrap-Parameter:**  
  Der Parameter `wrap_width` wird dynamisch an die aktuelle Fontgröße geknüpft, sodass der Text optimal umgebrochen wird. Falls du Probleme mit zu frühem oder zu spätem Umbrechen hast, kannst du diesen Ansatz im Code weiter anpassen.

- **Layout der A4-PDF-Seiten:**  
  Die Anordnung der Karten auf A4-Seiten (2×2-Raster) und die Reihenfolge (bei Rückseiten: 2 1 / 4 3) können im entsprechenden Abschnitt des PDF-Erstellungscodes modifiziert werden.
