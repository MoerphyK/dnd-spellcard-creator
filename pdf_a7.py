from reportlab.lib.pagesizes import portrait
from reportlab.pdfgen import canvas
import os
import csv


# --- Pfade und Dateien ---
OUTPUT_DIR = "output"
PDF_DIR = "pdf"
CSV_DIR = "csv"
CSV_PATH = os.path.join(CSV_DIR, "spells.csv")  # Deine CSV-Datei mit den Kartendaten


# Sicherstellen, dass der Ausgabeordner existiert
os.makedirs(PDF_DIR, exist_ok=True)

# --- A7 Format in Punkte (Breite x Höhe) ---
# (Hier als Portrait definiert)
A7_WIDTH = 210
A7_HEIGHT = 297
A7_SIZE = (A7_WIDTH, A7_HEIGHT)

# --- PDF-Dateiname ---
pdf_filename = os.path.join(PDF_DIR, "cards_double_sided_a7.pdf")

# --- Lies die CSV, um die Kartenreihenfolge zu erhalten ---
cards = []
with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Wir gehen davon aus, dass im Feld "Name" der Basisdateiname (ohne _front.png/_back.png) steht
        cards.append(row["Name"])

# --- Erzeuge das PDF ---
c = canvas.Canvas(pdf_filename, pagesize=A7_SIZE)

# Für jede Karte: Zuerst die Vorderseite, dann die Rückseite (beide als eigene Seiten)
for card in cards:
    # Erstelle die vollständigen Dateipfade
    front_img_path = os.path.join(OUTPUT_DIR, f"{card}_front.png")
    back_img_path  = os.path.join(OUTPUT_DIR, f"{card}_back.png")
    
    # Prüfe, ob die Dateien existieren (optional)
    if not os.path.exists(front_img_path):
        print(f"Warnung: Datei nicht gefunden: {front_img_path}")
        continue
    if not os.path.exists(back_img_path):
        print(f"Warnung: Datei nicht gefunden: {back_img_path}")
        continue

    # Seite 1: Vorderseite
    c.drawImage(front_img_path, 0, 0, width=A7_WIDTH, height=A7_HEIGHT)
    c.showPage()  # Neue Seite im PDF

    # Seite 2: Rückseite
    c.drawImage(back_img_path, 0, 0, width=A7_WIDTH, height=A7_HEIGHT)
    c.showPage()

# PDF speichern
c.save()
print(f"PDF erstellt: {pdf_filename}")
