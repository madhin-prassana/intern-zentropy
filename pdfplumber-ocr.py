import pdfplumber
from pdf2image import convert_from_path
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r"/opt/homebrew/bin/tesseract"
pdf_path = "sample_data/apple_data.pdf"
output_md = "output_data/pdfplumber-ocr(apple).md"

def is_gibberish(text):
    if not text or len(text.strip()) < 10:
        return True
    non_printable = sum(1 for c in text if not c.isprintable())
    return non_printable / len(text) > 0.3 or "(cid:" in text

with open(output_md, "w", encoding="utf-8") as md_file:
    with pdfplumber.open(pdf_path) as pdf:
        images = convert_from_path(pdf_path, poppler_path="/opt/homebrew/bin")

        for i, page in enumerate(pdf.pages):
            md_file.write(f"\n## Page {i + 1}\n\n")

            text = page.extract_text()

            if text and not is_gibberish(text):
                md_file.write(text + "\n\n")

                def clean_row(row):
                    return [str(cell) if cell is not None else "" for cell in row]

                tables = page.extract_tables()
                for table in tables:
                    header = clean_row(table[0])
                    md_file.write("| " + " | ".join(header) + " |\n")
                    md_file.write("|" + "|".join([" --- " for _ in header]) + "|\n")
                    for row in table[1:]:
                        cleaned_row = clean_row(row)
                        md_file.write("| " + " | ".join(cleaned_row) + " |\n")
                    md_file.write("\n")
            else:
                ocr_text = pytesseract.image_to_string(images[i])
                md_file.write("**OCR Extracted Text:**\n\n")
                md_file.write(ocr_text + "\n\n")

print("Markdown export complete. Check", output_md)