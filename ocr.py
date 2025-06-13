from pdf2image import convert_from_path
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
pdf_path = "/Users/madhinprassana/Downloads/TLA.pdf"
print("Parsing PDF...")
images = convert_from_path(pdf_path)
output_file = "/Users/madhinprassana/Downloads/TLA(output).txt"
with open(output_file, "w", encoding="utf-8") as f:
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image, lang='tam')
        f.write(f"\n### PAGE {i + 1} ###\n")
        f.write(text + "\n")

print(f"OCR text saved to {output_file}")

#Image OCR takes a more than a few minutes but provides good results and is completely offline.
#Probably best to refine this but it will take a lot of time as each run takes at least 5 minutes.