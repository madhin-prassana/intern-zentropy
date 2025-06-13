import os
from dotenv import load_dotenv
from pdf2image import convert_from_path
import pytesseract
import pdfplumber
from markitdown import MarkItDown

#LlamaParse
class LlamaParser:
    def __init__(self):
        from llama_parse import LlamaParse
        load_dotenv()
        api_key = os.getenv("LLAMA_CLOUD_API_KEY")
        self.parser = LlamaParse(result_type="markdown", verbose=True)

    def parse(self, pdf_path, output_path="output_data/amalgamation(llama).md"):
        documents = self.parser.load_data(pdf_path)
        with open(output_path, "w", encoding="utf-8") as f:
            for doc in documents:
                f.write(doc.text + "\n")
        print(f"\nParsed content saved to {output_path}")

# Marker
class MarkerParser:
    def parse(self, pdf_path, output_path="output_data/amalgamation(marker).md"):
        from marker.converters.pdf import PdfConverter
        from marker.models import create_model_dict
        from marker.output import text_from_rendered

        converter = PdfConverter(artifact_dict=create_model_dict())
        rendered = converter(pdf_path)
        text, _, _ = text_from_rendered(rendered)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Parsed content saved to {output_path}")


# Docling
class DoclingParser:
    def parse(self, pdf_path, output_path="output_data/amalgamation(docling).md"):
        from docling.document_converter import DocumentConverter

        print("Parsing PDF...")
        converter = DocumentConverter()
        result = converter.convert(pdf_path)
        markdown_content = result.document.export_to_markdown()

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        print(f"Parsed content saved to {output_path}")


# Markitdown
class MarkitdownParser:
    def __init__(self):
        self.md_parser = MarkItDown(enable_plugins=False)
        pytesseract.pytesseract.tesseract_cmd = r"/opt/homebrew/bin/tesseract"

    def parse(self, pdf_path, output_path="output_data/amalgamation(markitdown).md"):
        result = self.md_parser.convert(pdf_path)
        content = result.text_content.strip()

        if not content or len(content) < 50:
            print("Tesseract OCR fallback...")
            images = convert_from_path(pdf_path)
            content = ""
            for i, image in enumerate(images):
                ocr_text = pytesseract.image_to_string(image)
                content += f"\n--- Page {i + 1} (OCR Fallback) ---\n{ocr_text.strip()}\n"

        # Save to .md
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Markdown saved to {output_path}")

#Tesseract OCR only
class OCRParser:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r"/opt/homebrew/bin/tesseract"

    def parse(self, pdf_path, output_path="output_data/amalgamation(ocr).md"):
        images = convert_from_path(pdf_path)
        with open(output_path, "w", encoding="utf-8") as f:
            for i, image in enumerate(images):
                text = pytesseract.image_to_string(image)
                f.write(f"\n--- Page {i + 1} ---\n{text}\n")
        print(f"Parsed content saved to {output_path}")

#Tesseract OCR and PDFPlumber
class HybridParser:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r"/opt/homebrew/bin/tesseract"

    def is_gibberish(self, text):
        if not text or len(text.strip()) < 10:
            return True
        non_printable = sum(1 for c in text if not c.isprintable())
        return non_printable / len(text) > 0.3 or "(cid:" in text

    def parse(self, pdf_path, output_path="output_data/amalgamation(hybrid).md"):
        with open(output_path, "w", encoding="utf-8") as md_file:
            with pdfplumber.open(pdf_path) as pdf:
                images = convert_from_path(pdf_path, poppler_path="/opt/homebrew/bin")
                for i, page in enumerate(pdf.pages):
                    md_file.write(f"\n## Page {i + 1}\n\n")
                    text = page.extract_text()
                    if text and not self.is_gibberish(text):
                        md_file.write(text + "\n\n")
                        tables = page.extract_tables()
                        for table in tables:
                            header = [str(cell or "") for cell in table[0]]
                            md_file.write("| " + " | ".join(header) + " |\n")
                            md_file.write("|" + "|".join([" --- " for _ in header]) + "|\n")
                            for row in table[1:]:
                                cleaned = [str(cell or "") for cell in row]
                                md_file.write("| " + " | ".join(cleaned) + " |\n")
                            md_file.write("\n")
                    else:
                        ocr_text = pytesseract.image_to_string(images[i])
                        md_file.write("**OCR Extracted Text:**\n\n" + ocr_text + "\n")
        print(f"Parsed content saved to {output_path}")

def main():
    print("---PDF PARSING METHODS---")
    print("1. LlamaParse - Best performance but uses API via LlamaCloud and has page limits per day")
    print("2. Marker - Not recommended for image heavy documents with complex structure")
    print("3. Docling - Slightly better than marker but suffers the same issue")
    print("4. Markitdown - Requires OCR anyway so not any better than no. 6")
    print("5. Tesseract OCR - Best for image heavy documents (excluding no. 1) and different languages but takes a lot of time")
    print("6. PDFPlumber w/ Tesseract OCR - Logic is a bit off so again best to use with image heavy doc")
    choice = input("Enter choice (1-6): ").strip()
    pdf_path = input("Enter the full path to your PDF file: ").strip()

    if choice == "1":
        parser = LlamaParser()
    elif choice == "2":
        parser = MarkerParser()
    elif choice == "3":
        parser = DoclingParser()
    elif choice == "4":
        parser = MarkitdownParser()
    elif choice == "5":
        parser = OCRParser()
    elif choice == "6":
        parser = HybridParser()
    else:
        print("Invalid choice.")
        return

    parser.parse(pdf_path)


if __name__ == "__main__":
    main()