from docling.document_converter import DocumentConverter

converter = DocumentConverter()
pdf_path = "sample_data/apple_data.pdf"
print("Parsing PDF...")
result = converter.convert(pdf_path)
markdown_content = result.document.export_to_markdown()
output_path = "output_data/docling-parse(apple).md"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(markdown_content)

print(f"Markdown saved to {output_path}")