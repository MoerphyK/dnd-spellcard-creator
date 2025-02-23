import os
import csv
import argparse
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas

def create_pdf(output_filename, num_cols, num_rows, orientation):
    group_size = num_cols * num_rows  # Anzahl der Karten pro Seite

    # --- Seitenformat basierend auf der Orientierung ---
    if orientation.lower() == "landscape":
        page_size = landscape(A4)
    else:
        page_size = A4
    page_width, page_height = page_size

    # --- Layout-Parameter ---
    margin = 20   # Seitenrand
    gap_x = 10    # horizontaler Zwischenraum
    gap_y = 10    # vertikaler Zwischenraum

    # Verfügbare Fläche für das Raster:
    avail_width = page_width - 2 * margin - (num_cols - 1) * gap_x
    avail_height = page_height - 2 * margin - (num_rows - 1) * gap_y

    # Original A7-Karte (im Portrait) hat ca. 210 x 298 Punkte, Seitenverhältnis ca. 0.705 (210/298)
    aspect = 210 / 298

    # Berechne ideale Kartengröße:
    card_width = avail_width / num_cols
    card_height = card_width / aspect

    # Falls der Gesamthöhenbedarf zu hoch ist, skaliere entsprechend:
    total_card_height = card_height * num_rows + (num_rows - 1) * gap_y
    if total_card_height > avail_height:
        card_height = (avail_height - (num_rows - 1) * gap_y) / num_rows
        card_width = card_height * aspect

    # Gesamtgröße des Rasters:
    grid_width = num_cols * card_width + (num_cols - 1) * gap_x
    grid_height = num_rows * card_height + (num_rows - 1) * gap_y

    # Offsets zum Zentrieren des Rasters auf der Seite:
    offset_x = (page_width - grid_width) / 2.0
    offset_y = (page_height - grid_height) / 2.0

    # Berechne die Positionen im Raster (von unten links, Zeile für Zeile von links nach rechts):
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

    # --- Gruppiere Karten in Gruppen der Größe group_size ---
    groups = [cards[i:i+group_size] for i in range(0, len(cards), group_size)]
    if groups and len(groups[-1]) < group_size:
        groups[-1].extend([None] * (group_size - len(groups[-1])))

    # --- Definiere die Back-Order für jede Seite ---
    # Für jede Zeile im Raster (mit num_cols Karten) soll die Reihenfolge horizontal gespiegelt werden.
    # Beispiel: Für num_cols = 4, Zeile: [0,1,2,3] -> [3,2,1,0]. Für mehrere Zeilen wird dies zeilenweise angewendet.
    back_order = []
    for r in range(num_rows):
        row_indices = list(range(r * num_cols, r * num_cols + num_cols))
        back_order.extend(list(reversed(row_indices)))

    # --- Erzeuge das PDF ---
    pdf_filepath = os.path.join("pdf", output_filename)
    c = canvas.Canvas(pdf_filepath, pagesize=page_size)

    # Für jede Gruppe fügen wir zwei Seiten hinzu: eine für Vorderseiten und eine für Rückseiten.
    for group in groups:
        # --- Vorderseite (Front) ---
        for i, card in enumerate(group):
            if card is not None:
                front_img_path = os.path.join("output", f"{card}_front.png")
                if os.path.exists(front_img_path):
                    pos = positions[i]
                    c.drawImage(front_img_path, pos[0], pos[1], width=card_width, height=card_height)
                else:
                    print(f"Warnung: Datei nicht gefunden: {front_img_path}")
        c.showPage()

        # --- Rückseite (Back) ---
        for j, idx in enumerate(back_order):
            card = group[idx]
            if card is not None:
                back_img_path = os.path.join("output", f"{card}_back.png")
                if os.path.exists(back_img_path):
                    pos = positions[j]
                    c.drawImage(back_img_path, pos[0], pos[1], width=card_width, height=card_height)
                else:
                    print(f"Warnung: Datei nicht gefunden: {back_img_path}")
        c.showPage()

    c.save()
    print(f"PDF erstellt: {pdf_filepath}")

def main():
    parser = argparse.ArgumentParser(
        description="Erzeuge ein doppelseitiges PDF mit dynamischer Anzahl an Karten pro Seite und wählbarer Orientierung."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="cards_double_sided_dynamic.pdf",
        help="Name der Ausgabedatei (PDF). Standard: cards_double_sided_dynamic.pdf"
    )
    parser.add_argument("--cols", type=int, default=3, help="Anzahl der Spalten pro Seite (default: 3)")
    parser.add_argument("--rows", type=int, default=3, help="Anzahl der Zeilen pro Seite (default: 3)")
    parser.add_argument(
        "--orientation",
        type=str,
        choices=["portrait", "landscape"],
        default="portrait",
        help="Ausrichtung der Seite (default: portrait)"
    )
    args = parser.parse_args()
    create_pdf(args.output, args.cols, args.rows, args.orientation)

if __name__ == "__main__":
    main()
