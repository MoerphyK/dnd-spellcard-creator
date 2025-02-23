import os
import csv
import argparse
import sys
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def draw_guidelines(c, positions, card_width, card_height, page_width, page_height):
    """
    Zeichnet gestrichelte Hilfslinien an allen Kanten des Kartenrasters, 
    die über die gesamte Seitenbreite bzw. -höhe verlaufen.
    """
    # Bestimme alle eindeutigen vertikalen und horizontalen Kanten aus den Kartenpositionen
    verticals = set()
    horizontals = set()
    for (x, y) in positions:
        verticals.add(x)
        verticals.add(x + card_width)
        horizontals.add(y)
        horizontals.add(y + card_height)
    verticals = sorted(verticals)
    horizontals = sorted(horizontals)
    
    c.setDash(3, 3)
    c.setStrokeColorRGB(0, 0, 0)
    for x in verticals:
        c.line(x, 0, x, page_height)
    for y in horizontals:
        c.line(0, y, page_width, y)
    c.setDash([])

def draw_borders(c, group, positions, card_width, card_height):
    """
    Zeichnet um jede vorhandene Karte einen 2-mm breiten schwarzen Rand.
    """
    # 2 mm in Punkte: 2 * (72/25.4) ≈ 5.67 Punkte
    border = 1.5 * 72 / 25.4
    c.setLineWidth(border)
    c.setStrokeColorRGB(0, 0, 0)
    for i, card in enumerate(group):
        if card is not None:
            pos = positions[i]
            c.rect(pos[0] - border, pos[1] - border, card_width + 2 * border, card_height + 2 * border, stroke=1, fill=0)

def create_pdf(output_filename, num_cols, num_rows, orientation):
    group_size = num_cols * num_rows  # Anzahl der Karten pro Seite

    # --- Seitenformat basierend auf der Orientierung ---
    # Für 3x3 Karten empfiehlt sich in der Regel das Portrait-Format.
    if orientation.lower() == "landscape":
        page_size = (A4[1], A4[0])
    else:
        page_size = A4
    page_width, page_height = page_size

    # --- Feste Kartengröße in mm umgerechnet in Punkte ---
    # 63,5 mm x 88,5 mm:
    card_width = 63.5 * 72 / 25.4   # ≈ 180 Punkte
    card_height = 88.5 * 72 / 25.4  # ≈ 250.5 Punkte

    # --- Layout-Parameter in Punkten ---
    margin = 1   # Seitenrand
    gap_x = 10    # horizontaler Zwischenraum zwischen den Karten
    gap_y = 10    # vertikaler Zwischenraum zwischen den Karten

    # --- Berechne die Gesamtgröße des Rasters ---
    grid_width = num_cols * card_width + (num_cols - 1) * gap_x
    grid_height = num_rows * card_height + (num_rows - 1) * gap_y

    # Überprüfe, ob das Raster (plus 2*margin) in die Seite passt:
    if grid_width > (page_width - 2 * margin) or grid_height > (page_height - 2 * margin):
        sys.exit("Fehler: Das Raster (mit den gewählten Spalten/Zeilen und festen Kartengrößen) passt nicht auf die Seite.")

    # Berechne Offsets, um das Raster zentriert auf der Seite zu platzieren:
    offset_x = (page_width - grid_width) / 2.0
    offset_y = (page_height - grid_height) / 2.0

    # --- Berechne die Positionen im Raster (von unten links, Zeile für Zeile von links nach rechts) ---
    positions = []
    for row in range(num_rows):
        for col in range(num_cols):
            x = offset_x + col * (card_width + gap_x)
            y = offset_y + row * (card_height + gap_y)
            positions.append((x, y))

    # --- Lese die CSV, um die Kartenbasisnamen zu erhalten ---
    cards = []
    CSV_PATH = os.path.join("csv", "spells.csv")
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cards.append(row["Name"])

    # Gruppiere Karten in Gruppen der Größe group_size:
    groups = [cards[i:i+group_size] for i in range(0, len(cards), group_size)]
    if groups and len(groups[-1]) < group_size:
        groups[-1].extend([None] * (group_size - len(groups[-1])))

    # --- Definiere die Back-Order für das Raster ---
    # Für jede Zeile (mit num_cols Karten) sollen die Karten in der Rückseite horizontal gespiegelt werden.
    # Bei einem 3x3-Raster:
    # Untere Zeile (Indices 0 bis 2): [2, 1, 0]
    # Mittlere Zeile (Indices 3 bis 5): [5, 4, 3]
    # Obere Zeile (Indices 6 bis 8): [8, 7, 6]
    back_order = []
    for r in range(num_rows):
        row_indices = list(range(r * num_cols, r * num_cols + num_cols))
        back_order.extend(list(reversed(row_indices)))

    # --- Erzeuge das PDF ---
    pdf_filepath = os.path.join("pdf", output_filename)
    c = canvas.Canvas(pdf_filepath, pagesize=page_size)

    # Optional: Füllung für den Rasterbereich erweitern (schwarz) – z. B. um 2 mm
    extra = 1.5 * 72 / 25.4

    for group in groups:
        # --- Vorderseite (Front) ---
        c.setFillColorRGB(0, 0, 0)
        c.rect(offset_x - extra, offset_y - extra, grid_width + 2 * extra, grid_height + 2 * extra, fill=1, stroke=0)
        for i, card in enumerate(group):
            if card is not None:
                front_img_path = os.path.join("output", f"{card}_front.png")
                if os.path.exists(front_img_path):
                    pos = positions[i]
                    c.drawImage(front_img_path, pos[0], pos[1], width=card_width, height=card_height)
                else:
                    print(f"Warnung: Datei nicht gefunden: {front_img_path}")
        draw_guidelines(c, positions, card_width, card_height, page_width, page_height)
        draw_borders(c, group, positions, card_width, card_height)
        c.showPage()

        # --- Rückseite (Back) ---
        c.setFillColorRGB(0, 0, 0)
        c.rect(offset_x - extra, offset_y - extra, grid_width + 2 * extra, grid_height + 2 * extra, fill=1, stroke=0)
        for j, idx in enumerate(back_order):
            card = group[idx]
            if card is not None:
                back_img_path = os.path.join("output", f"{card}_back.png")
                if os.path.exists(back_img_path):
                    pos = positions[j]
                    c.drawImage(back_img_path, pos[0], pos[1], width=card_width, height=card_height)
                else:
                    print(f"Warnung: Datei nicht gefunden: {back_img_path}")
        draw_guidelines(c, positions, card_width, card_height, page_width, page_height)
        draw_borders(c, group, positions, card_width, card_height)
        c.showPage()

    c.save()
    print(f"PDF erstellt: {pdf_filepath}")

def main():
    parser = argparse.ArgumentParser(
        description="Erzeuge ein doppelseitiges PDF mit fester Kartengröße (63.5mm x 88.5mm), erweiterten 2mm schwarzen Kartenrändern, "
                    "schwarz gefüllten Zwischenräumen im Raster und Hilfslinien, die über die gesamte Seite verlaufen. "
                    "Der Rasterbereich kann optional um 2mm erweitert werden, um auch am oberen und unteren Rand vollständig schwarz zu sein."
    )
    parser.add_argument("-o", "--output", type=str, default="cards_double_sided_3x3_cut.pdf",
                        help="Name der Ausgabedatei (PDF). Standard: cards_double_sided_3x3_cut.pdf")
    parser.add_argument("--cols", type=int, default=3, help="Anzahl der Spalten pro Seite (default: 3)")
    parser.add_argument("--rows", type=int, default=3, help="Anzahl der Zeilen pro Seite (default: 3)")
    parser.add_argument("--orientation", type=str, choices=["portrait", "landscape"], default="portrait",
                        help="Ausrichtung der Seite (default: portrait)")
    args = parser.parse_args()
    create_pdf(args.output, args.cols, args.rows, args.orientation)

if __name__ == "__main__":
    main()
