from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
import os
import csv

# --- Pfade und Dateien ---
OUTPUT_DIR = "output"
PDF_DIR = "pdf"
CSV_DIR = "csv"

os.makedirs(PDF_DIR, exist_ok=True)

# --- A4 in Landscape (Seitenmaße in Punkten) ---
page_width, page_height = landscape(A4)  # z. B. ca. 842 x 595 Punkte

# --- Layout-Parameter für 8 Karten pro Seite (4 Spalten, 2 Zeilen) ---
margin = 20         # Seitenrand in Punkten
gap_x = 10          # horizontaler Zwischenraum
gap_y = 10          # vertikaler Zwischenraum

# Verfügbare Fläche:
avail_width = page_width - 2 * margin - 3 * gap_x  # 4 Karten -> 3 Zwischenräume
avail_height = page_height - 2 * margin - 1 * gap_y  # 2 Karten -> 1 Zwischenraum

# Original A7-Karte (im Portrait) hat ca. 210 x 298 Punkte, also ein Seitenverhältnis von ca. 0.705 (210/298).
aspect = 210 / 298

# Da wir 8 Karten pro Seite anordnen möchten, berechnen wir:
# - 4 Karten pro Zeile: ideale Kartenbreite = avail_width / 4
ideal_card_width = avail_width / 4.0
# - Kartenhöhe so, dass das Seitenverhältnis erhalten bleibt:
ideal_card_height = ideal_card_width / aspect

# Falls 2 Reihen (ideal_card_height * 2 + gap_y) größer als avail_height werden,
# skaliere entsprechend:
if 2 * ideal_card_height + gap_y > avail_height:
    ideal_card_height = (avail_height - gap_y) / 2.0
    ideal_card_width = ideal_card_height * aspect

card_width = ideal_card_width
card_height = ideal_card_height

# --- Berechne die Positionen im 4x2-Raster ---
# Das Raster wird von unten links (Position 0) aus aufgebaut, Zeile für Zeile von links nach rechts.
positions = []
for row in range(2):  # 2 Zeilen (row 0: untere Zeile, row 1: obere Zeile)
    for col in range(4):  # 4 Spalten (von links nach rechts)
        x = margin + col * (card_width + gap_x)
        y = margin + row * (card_height + gap_y)
        positions.append((x, y))
# positions[0] entspricht der untersten linken Karte, positions[1] der nächsten rechts, usw.

# --- Lese die CSV, um die Reihenfolge (Basisnamen) der Karten zu erhalten ---
cards = []
CSV_PATH = os.path.join(CSV_DIR, "spells.csv")
with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cards.append(row["Name"])

# --- Gruppiere Karten in Gruppen von 8 ---
groups = [cards[i:i+8] for i in range(0, len(cards), 8)]
if groups and len(groups[-1]) < 8:
    groups[-1].extend([None] * (8 - len(groups[-1])))

# --- Definiere die Back-Order ---
# Für jede Gruppe (Indices 0 bis 7) sollen die Karten in jeder Zeile horizontal gespiegelt werden:
# Untere Zeile: aus [0,1,2,3] → [3,2,1,0]
# Obere Zeile: aus [4,5,6,7] → [7,6,5,4]
back_order = [3, 2, 1, 0, 7, 6, 5, 4]

# --- Erzeuge das PDF ---
pdf_filename = os.path.join(PDF_DIR, "cards_double_sided_8_per_page.pdf")
c = canvas.Canvas(pdf_filename, pagesize=landscape(A4))

# Für jede Gruppe fügen wir zwei Seiten hinzu: eine für die Vorderseiten und eine für die Rückseiten.
for group in groups:
    # --- Vorderseite (Front) ---
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
    # Keine Rotation mehr – stattdessen verwenden wir die definierte Back-Order, um jede Zeile horizontal zu spiegeln.
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
