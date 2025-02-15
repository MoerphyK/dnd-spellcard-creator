import PyPDF2

# Öffne beide PDF-Dateien im Lese-Binärmodus
with open("Datei1.pdf", "rb") as file1, open("Datei2.pdf", "rb") as file2:
    pdf1 = PyPDF2.PdfReader(file1)
    pdf2 = PyPDF2.PdfReader(file2)
    writer = PyPDF2.PdfWriter()
    
    # Ermittle die Anzahl der Seiten, die in beiden PDFs vorhanden sind
    num_pages = min(len(pdf1.pages), len(pdf2.pages))
    
    # Füge abwechselnd Seiten aus beiden PDFs hinzu
    for i in range(num_pages):
        writer.add_page(pdf1.pages[i])
        writer.add_page(pdf2.pages[i])
    
    # Falls eine PDF mehr Seiten hat, füge die restlichen Seiten hinten an
    if len(pdf1.pages) > num_pages:
        for page in pdf1.pages[num_pages:]:
            writer.add_page(page)
    elif len(pdf2.pages) > num_pages:
        for page in pdf2.pages[num_pages:]:
            writer.add_page(page)
    
    # Schreibe das Ergebnis in eine neue PDF-Datei
    with open("merged.pdf", "wb") as output_file:
        writer.write(output_file)
