from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import csv

# --- Pfade und Dateien ---
OUTPUT_DIR = "output"
PDF_DIR = "pdf"
CSV_DIR = "csv"

# Sicherstellen, dass der Ausgabeordner existiert
os.makedirs(PDF_DIR, exist_ok=True)

# --- Seitenmaße in Punkten (A4) ---
page_width, page_height = A4  # A4 ca. 595 x 842 Punkte

# --- A7-Kartengröße in Punkten (ca. 210 x 298 Punkte) ---
card_width = 210
card_height = 298

# --- Berechne horizontale und vertikale Lücken (grob) ---
# Es gibt 2 Karten pro Reihe, also 3 Lücken (linker Rand, Zwischenraum, rechter Rand)
gap_x = (page_width - 2 * card_width) / 3.0
gap_y = (page_height - 2 * card_height) / 3.0

# --- Definiere die Positionen (unten links der Karte) im 2×2-Raster ---
positions = [
    (gap_x, gap_y),                                      # Position A: untere linke Karte
    (2 * gap_x + card_width, gap_y),                     # Position B: untere rechte Karte
    (gap_x, 2 * gap_y + card_height),                    # Position C: obere linke Karte
    (2 * gap_x + card_width, 2 * gap_y + card_height)      # Position D: obere rechte Karte
]

# --- Lese die CSV, um die Reihenfolge (Basisnamen) der Karten zu erhalten ---
cards = []
CSV_PATH = os.path.join(CSV_DIR, "spells.csv")
with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Wir gehen davon aus, dass im Feld "Name" der Basisdateiname steht
        cards.append(row["Name"])

# --- Gruppiere Karten in Vierergruppen ---
groups = [cards[i:i+4] for i in range(0, len(cards), 4)]
# Falls die letzte Gruppe weniger als 4 Karten enthält, auffüllen:
if len(groups[-1]) < 4:
    groups[-1].extend([None] * (4 - len(groups[-1])))

# --- Erzeuge das PDF ---
pdf_filename = os.path.join(PDF_DIR, "cards_double_sided.pdf")
c = canvas.Canvas(pdf_filename, pagesize=A4)

# Für die Rückseite wollen wir die Reihenfolge ändern:
# Wir definieren die gewünschte Back-Order: an Position A (unten links) soll Karte 2,
# Position B (unten rechts) Karte 1, Position C (oben links) Karte 4 und Position D (oben rechts) Karte 3.
back_order = [1, 0, 3, 2]

# Für jede Gruppe fügen wir zwei Seiten hinzu: eine für Vorderseiten und eine für Rückseiten.
for group in groups:
    # --- Vorderseite (Front) ---
    # Zeichne die Karten in der Reihenfolge [Karte 1, Karte 2, Karte 3, Karte 4] an den definierten Positionen.
    for i, card in enumerate(group):
        if card is not None:
            front_img_path = os.path.join(OUTPUT_DIR, f"{card}_front.png")
            if os.path.exists(front_img_path):
                pos = positions[i]
                c.drawImage(front_img_path, pos[0], pos[1], width=card_width, height=card_height)
            else:
                print(f"Warnung: Datei nicht gefunden: {front_img_path}")
    c.showPage()  # Seite für die Vorderseiten abschließen

    # --- Rückseite (Back) ---
    # Verwende die gewünschte Reihenfolge: [Karte 2, Karte 1, Karte 4, Karte 3].
    for j, idx in enumerate(back_order):
        card = group[idx]
        if card is not None:
            back_img_path = os.path.join(OUTPUT_DIR, f"{card}_back.png")
            if os.path.exists(back_img_path):
                pos = positions[j]
                c.drawImage(back_img_path, pos[0], pos[1], width=card_width, height=card_height)
            else:
                print(f"Warnung: Datei nicht gefunden: {back_img_path}")
    c.showPage()  # Seite für die Rückseiten abschließen

c.save()
print(f"PDF erstellt: {pdf_filename}")
