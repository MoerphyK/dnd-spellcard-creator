from PIL import Image, ImageDraw, ImageFont
import csv
import os
import textwrap

# --------------------------
# Pfade zu den Assets
# --------------------------
ASSETS_DIR = "assets"
ILLUSTRATIONS_DIR = os.path.join(ASSETS_DIR, "illustrations")
OUTPUT_DIR = "output"
CSV_DIR    = "csv"

# Sicherstellen, dass der Ausgabeordner existiert
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------------
# Lade die Basisbilder
# --------------------------
front_bg = Image.open(os.path.join(ASSETS_DIR, "front_background.png")).convert("RGBA")
back_bg = Image.open(os.path.join(ASSETS_DIR, "back_background.png")).convert("RGBA")
spellname_banner = Image.open(os.path.join(ASSETS_DIR, "spellname_banner.png")).convert("RGBA")
# illustration = Image.open(os.path.join(ASSETS_DIR, "illustration.png")).convert("RGBA")
front_frame = Image.open(os.path.join(ASSETS_DIR, "front_frame.png")).convert("RGBA")

# --------------------------
# Klassenbanner in ein Dictionary laden
# --------------------------
class_names = [
    "Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk",
    "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"
]
class_banners = {}
for cls in class_names:
    # Beispiel: Dateiname im Format "wizard.png", "warlock.png" usw.
    filename = f"{cls.lower()}.png"
    path = os.path.join(ASSETS_DIR, "class_banners", filename)
    if os.path.exists(path):
        class_banners[cls] = Image.open(path).convert("RGBA")
    else:
        print(f"Warnung: Banner für {cls} nicht gefunden unter {path}")

# --------------------------
# Schriftarten laden
# --------------------------
FONT_PATH = os.path.join(ASSETS_DIR, "fonts", "UNISPACE_BD.ttf")
title_font = ImageFont.truetype(FONT_PATH, 36)
detail_font = ImageFont.truetype(FONT_PATH, 24)

# --------------------------
# Hilfsfunktion: Textgröße ermitteln
# --------------------------
def get_text_size(draw, text, font):
    """
    Versucht, die Textgröße mittels draw.textbbox zu ermitteln.
    Falls das nicht verfügbar ist, wird font.getsize als Fallback genutzt.
    """
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return width, height
    except AttributeError:
        return font.getsize(text)

# --------------------------
# Hilfsfunktion: Optimale Schriftgröße finden
# --------------------------
def find_optimal_font_size(draw, text, font_path, min_font_size, max_font_size, max_width, max_height, line_spacing, paragraph_spacing):
    """
    Sucht den größtmöglichen Font-Wert zwischen min_font_size und max_font_size,
    sodass der umgebrochene Text (bei dynamisch berechnetem wrap_width) in den Bereich passt.
    """
    def get_lines_for_font(font, text):
        # Berechne den effektiven wrap_width für die aktuelle Font
        eff_wrap = effective_wrap_width(draw, font, max_width)
        paragraphs = text.splitlines()
        lines = []
        for para in paragraphs:
            if para.strip():
                wrapped = textwrap.wrap(para, width=eff_wrap)
                lines.extend(wrapped)
            else:
                lines.append(None)
        return lines

    def lines_fit(font, lines):
        return all(get_text_size(draw, line, font)[0] <= max_width for line in lines if line is not None)

    def total_text_height(font, lines):
        total = 0
        for line in lines:
            if line is None:
                total += paragraph_spacing
            else:
                total += get_text_size(draw, line, font)[1] + line_spacing
        if total > 0:
            total -= line_spacing
        return total

    low = min_font_size
    high = max_font_size
    best = low
    while low <= high:
        mid = (low + high) // 2
        font = ImageFont.truetype(font_path, mid)
        lines = get_lines_for_font(font, text)
        if lines_fit(font, lines) and total_text_height(font, lines) <= max_height:
            best = mid  # Dieser Wert passt; versuche einen größeren Font
            low = mid + 1
        else:
            high = mid - 1
    return best

# --------------------------
# Hilfsfunktion: Effektive Umbruchbreite
# --------------------------
def effective_wrap_width(draw, font, max_width):
    # Bestimme die Breite eines typischen Zeichens, z. B. "M"
    char_width, _ = get_text_size(draw, "M", font)
    if char_width == 0:
        return 1
    return max(1, int(max_width // char_width))


# --------------------------
# Funktion: Text an vorgegebener Position zentriert zeichnen
# --------------------------
def draw_text_centered_at(draw, center, text, font_path, max_width, max_height, max_font_size, fill="black", wrap_width=20):
    """
    Zeichnet den übergebenen Text zentriert um die Position 'center' (x, y) auf dem Bild,
    sodass die Breite des Textes maximal 'max_width' und die Gesamthöhe maximal 'max_height' nicht überschreitet.
    
    Der Text wird zunächst umgebrochen (wrap_width gibt an, nach wie vielen Zeichen umgebrochen wird)
    und die Schriftgröße wird dynamisch reduziert, bis alle Zeilen in max_width passen und der gesamte
    Textblock die max_height nicht überschreitet.
    
    Parameter:
      - draw: Das ImageDraw-Objekt, auf dem gezeichnet wird.
      - center: Tuple (x, y), der Mittelpunkt des Textblocks.
      - text: Der darzustellende Text.
      - font_path: Pfad zur TTF-Schriftdatei.
      - max_width: Maximale erlaubte Breite des Textblocks in Pixel.
      - max_height: Maximale erlaubte Höhe des Textblocks in Pixel.
      - max_font_size: Start-Schriftgröße, die ggf. reduziert wird.
      - fill: Textfarbe.
      - wrap_width: Maximale Anzahl Zeichen pro Zeile (für den automatischen Zeilenumbruch).
    """
    # Text umbrechen
    wrapped_text = "\n".join(textwrap.wrap(text, width=wrap_width))
    font_size = max_font_size
    font = ImageFont.truetype(font_path, font_size)
    lines = wrapped_text.split('\n')
    
    # Funktion zur Überprüfung, ob jede Zeile in max_width passt
    def lines_fit(font):
        return all(get_text_size(draw, line, font)[0] <= max_width for line in lines)
    
    # Funktion zur Berechnung der Gesamthöhe des Textblocks
    def total_text_height(font):
        return sum(get_text_size(draw, line, font)[1] for line in lines)
    
    # Schriftgröße reduzieren, bis alle Zeilen passen und der Textblock in max_height passt
    while (not lines_fit(font) or total_text_height(font) > max_height) and font_size > 10:
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
    
    total_height = total_text_height(font)
    start_y = center[1] - total_height // 2
    
    # Jede Zeile horizontal zentriert zeichnen
    for line in lines:
        text_width, text_height = get_text_size(draw, line, font)
        start_x = center[0] - text_width // 2
        draw.text((start_x, start_y), line, font=font, fill=fill)
        start_y += text_height


def draw_text_left_aligned_at(draw, top_left, text, font_path, max_width, max_height, max_font_size, fill="black",
                              max_wrap_width=1000, line_spacing=2, paragraph_spacing=10, min_font_size=10):
    """
    Zeichnet den übergebenen Text linksbündig innerhalb eines definierten Bereichs.
    
    Der Text wird zunächst in Absätze aufgeteilt und anschließend mittels textwrap.wrap
    unter Verwendung eines dynamisch berechneten wrap_width (abhängig von der Fontgröße)
    in Zeilen aufgeteilt. Danach wird mittels einer binären Suche der größtmögliche Font-Wert
    (zwischen min_font_size und max_font_size) ermittelt, der den gesamten Text (inklusive
    Zeilen- und Absatzabständen) in den Bereich (max_width x max_height) passen lässt.
    
    Der Text wird dann von oben beginnend linksbündig gezeichnet.
    """
    # Finde die optimale Fontgröße mithilfe der dynamischen Berechnung des wrap_width:
    optimal_size = find_optimal_font_size(draw, text, font_path, min_font_size, max_font_size, max_width, max_height, line_spacing, paragraph_spacing)
    font = ImageFont.truetype(font_path, optimal_size)
    
    # Berechne nun den effektiven wrap_width für die gefundene Font:
    eff_wrap = effective_wrap_width(draw, font, max_width)
    # Wenn der Text keine Zeilenumbrüche enthält, könnten wir ihn in einer Zeile belassen:
    # Hier erlauben wir aber maximal max_wrap_width als Obergrenze.
    if "\n" not in text and len(text) < eff_wrap:
        eff_wrap = max_wrap_width
    
    # Teile den Text in Zeilen auf (unter Beachtung von vorhandenen Newlines)
    paragraphs = text.splitlines()
    lines = []
    for para in paragraphs:
        if para.strip():
            wrapped = textwrap.wrap(para, width=eff_wrap)
            lines.extend(wrapped)
        else:
            lines.append(None)
    
    current_y = top_left[1]
    for line in lines:
        if line is None:
            current_y += paragraph_spacing
        else:
            text_width, text_height = get_text_size(draw, line, font)
            current_x = top_left[0]
            draw.text((current_x, current_y), line, font=font, fill=fill)
            current_y += text_height + line_spacing


# --------------------------
# Hauptfunktion: Karte erstellen
# --------------------------
def create_card(spell_data):
    spell_name = spell_data["Name"]
    
    # --------------------------
    # Seite A: Vorderseite
    # --------------------------
    front = front_bg.copy()
    illustration_pos = (126, 221)
    
    # 1. Illustration einfügen
    illustration_filename = f"{spell_name.lower().replace(' ', '_')}.jpg"
    illustration_path = os.path.join(ILLUSTRATIONS_DIR, illustration_filename)
    # Prüfen, ob die Illustration für den Spell vorhanden ist
    if os.path.exists(illustration_path):
        illu_image = Image.open(illustration_path).convert("RGBA")
        # Skaliere die Illustration auf 556x556 Pixel (ohne Zuschneiden)
        illu_image = illu_image.resize((556, 556), Image.Resampling.LANCZOS)
        # Neue Top-Left-Position: (163, 236)
        illustration_pos = (163, 236)
        front.paste(illu_image, illustration_pos, illu_image)
    else:
        print(f"Illustration für {spell_name} nicht gefunden.")
    
    # 2. Front-Frame überlagern
    front.paste(front_frame, (0, 0), front_frame)
    
    # 3. Klassenbanner hinzufügen
    # Angenommen, das CSV-Feld "Classes" enthält Klassen als kommaseparierte Liste
    classes_str = spell_data["Classes"]
    if classes_str:
        spell_classes = [s.strip() for s in classes_str.split(",")]
        for cls in spell_classes:
            if cls in class_banners:
                banner = class_banners[cls]
                front.paste(banner, (0, 0), banner)
            else:
                print(f"Kein Banner für Klasse '{cls}' gefunden.")
    
    # 4. Spellname Banner vorbereiten und modifizieren
    banner_copy = spellname_banner.copy()
    draw_banner = ImageDraw.Draw(banner_copy)
    # Zentriere den Titel im Banner so, dass der Mittelpunkt bei (banner.width/2, 135) liegt.
    center_banner = (banner_copy.width // 2, 135)
    # max_width im Banner: Bannerbreite minus Ränder (z.B. 40 Pixel)
    max_width_banner = banner_copy.width - 40
    draw_text_centered_at(draw_banner, center_banner, spell_name, FONT_PATH, max_width_banner, max_height=90, max_font_size=36, fill="black", wrap_width=20)
    
    # Das modifizierte Banner an der gewünschten Position einfügen.
    banner_pos = (0, 0)
    front.paste(banner_copy, banner_pos, banner_copy)
    
    # 5. Weitere Infos auf der Vorderseite hinzufügen
    draw_front = ImageDraw.Draw(front)
    
    ## Spell Level
    center_spell_level = (155, 1050)
    text_spell_level = spell_data["Level"]
    if text_spell_level == "Cantrip":
        text_spell_level = "0"
    if text_spell_level[-2:] in ["st", "nd", "rd", "th"]:
        text_spell_level = text_spell_level[:-2]
    draw_text_centered_at(draw_front, center_spell_level, text_spell_level, FONT_PATH,
                      max_width=90, max_height=85, max_font_size=60, fill="black", wrap_width=20)

    ## Info Boxen
    # Wir definieren hier eine maximale Breite und Schriftgröße für diese Infos (anpassbar)
    max_width_info = 140
    max_height_info = 40
    max_font_info = 24
    wrap_width_info = 18  # meist kein Zeilenumbruch nötig, kann aber angepasst werden

    ## Obere Reihe (y = 1009)
    # Casting Time links
    center_casting_time = (445, 1009)
    text_casting_time = spell_data["Casting Time"]
    draw_text_centered_at(draw_front, center_casting_time, text_casting_time, FONT_PATH,
                      max_width=max_width_info, max_height=max_height_info, max_font_size=max_font_info, fill="black", wrap_width=wrap_width_info)

    ## Duration rechts
    center_duration = (692, 1009)
    text_duration = spell_data["Duration"]
    draw_text_centered_at(draw_front, center_duration, text_duration, FONT_PATH,
                        max_width=max_width_info, max_height=max_height_info, max_font_size=max_font_info, fill="black", wrap_width=wrap_width_info)

    ## Untere Reihe (y = 1132)
    # Range links
    center_range = (445, 1132)
    text_range = spell_data["Range"]
    draw_text_centered_at(draw_front, center_range, text_range, FONT_PATH, 
                          max_width=max_width_info, max_height=max_height_info, max_font_size=max_font_info, fill="black", wrap_width=wrap_width_info)

    # Components rechts
    center_components = (692, 1132)
    # Wenn die Komponenten M vorhanden sind, dann sollen die Materialkomponenten nicht gelistet werden.
    text_components = spell_data["Components"]
    if "(" in text_components and ")" in text_components:
        text_components = text_components.split("(")[0].strip()
    draw_text_centered_at(draw_front, center_components, text_components, FONT_PATH,
                      max_width=max_width_info, max_height=max_height_info, max_font_size=max_font_info, fill="black", wrap_width=wrap_width_info)

    # Speichere die Vorderseite
    front_filename = os.path.join(OUTPUT_DIR, f"{spell_name}_front.png")
    front.save(front_filename)
    print(f"Vorderseite gespeichert: {front_filename}")

    # --------------------------
    # Seite B: Rückseite
    # --------------------------
    back = back_bg.copy()
    draw_back = ImageDraw.Draw(back)
    
    # 1. Klassenbanner hinzufügen
    # Angenommen, das CSV-Feld "Classes" enthält Klassen als kommaseparierte Liste
    classes_str = spell_data["Classes"]
    if classes_str:
        spell_classes = [s.strip() for s in classes_str.split(",")]
        for cls in spell_classes:
            if cls in class_banners:
                banner = class_banners[cls]
                back.paste(banner, (0, 0), banner)
            else:
                print(f"Kein Banner für Klasse '{cls}' gefunden.")
    
    # 2. Spellname Banner vorbereiten und modifizieren
    banner_copy = spellname_banner.copy()
    draw_banner = ImageDraw.Draw(banner_copy)
    # Zentriere den Titel im Banner so, dass der Mittelpunkt bei (banner.width/2, 135) liegt.
    center_banner = (banner_copy.width // 2, 135)
    # max_width im Banner: Bannerbreite minus Ränder (z.B. 40 Pixel)
    max_width_banner = banner_copy.width - 40
    draw_text_centered_at(draw_banner, center_banner, spell_name, FONT_PATH, max_width_banner, max_height=90, max_font_size=36, fill="black", wrap_width=20)
    
    # Das modifizierte Banner an der gewünschten Position einfügen.
    banner_pos = (0, 0)
    back.paste(banner_copy, banner_pos, banner_copy)

    # Erster Teil: Statische Key-Informationen
    info_text = (
        f"Level:         {spell_data['Level']}\n"
        f"Casting Time:  {spell_data['Casting Time']}\n"
        f"Duration:      {spell_data['Duration']}\n"
        f"Range:         {spell_data['Range']}\n"
        f"Components:    {spell_data['Components']}\n"
        f"Classes:       {spell_data['Classes']}"
    )

    # Füge einen festen Abstand zwischen den beiden Bereichen ein, z. B. 20 Pixel
    gap = 10

    # Definiere den Bereich für den ersten Teil
    info_box_top_left = (95, 236)       # Obere linke Ecke der Info-Box
    info_box_max_width = 693            # Maximale Breite der Info-Box (anpassen)
    info_box_max_height = 175           # Maximale Höhe der Info-Box (anpassen)
    info_box_max_font_size = 32         # Start-Schriftgröße für diesen Bereich
    wrap_width_info = 60                # Wrap-Wert, je nach durchschnittlicher Zeichenlänge

    draw_text_left_aligned_at(draw_back, info_box_top_left, info_text, FONT_PATH,
                            max_width=info_box_max_width, max_height=info_box_max_height,
                            max_font_size=info_box_max_font_size, fill="black",
                            line_spacing=2, paragraph_spacing=20)

    # Wenn At Higher Levels vorhanden ist, füge es hinzu
    if spell_data["At Higher Levels"]:
        description_text = (
            f"Description:\n{spell_data['Text']}\n\n\n"
            f"At Higher Levels:\n{spell_data['At Higher Levels']}"
        )
    else:
        description_text = f"Description:\n{spell_data['Text']}"

    # Berechne den neue obere linke Ecke für den zweiten Teil
    # Hier gehen wir davon aus, dass der zweite Bereich direkt unter dem ersten beginnen soll.
    description_box_top_left = (info_box_top_left[0], info_box_top_left[1] + info_box_max_height + gap)
    description_box_max_width = 693         # Maximale Breite für den Beschreibungstext (anpassen)
    description_box_max_height = 700        # Maximale Höhe für den Beschreibungstext (anpassen)
    description_box_max_font_size = 40        # Start-Schriftgröße für diesen Bereich
    
    draw_text_left_aligned_at(draw_back, description_box_top_left, description_text, FONT_PATH,
                           max_width=description_box_max_width, max_height=description_box_max_height,
                           max_font_size=description_box_max_font_size, fill="black",
                           line_spacing=1)


    # Speichere die Rückseite
    back_filename = os.path.join(OUTPUT_DIR, f"{spell_name}_back.png")
    back.save(back_filename)
    print(f"Rückseite gespeichert: {back_filename}")

# --------------------------
# CSV einlesen und Karten erstellen
# --------------------------
CSV_PATH = os.path.join(CSV_DIR, "spells.csv")  # Pfad zu deiner CSV-Datei
with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for spell in reader:
        create_card(spell)
